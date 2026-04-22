#!/usr/bin/env python3
"""
Website UI Cloner (structure + style extraction)

What this tool does:
- Fetches a target page (HTML + linked stylesheets)
- Extracts design signals (colors, typography, spacing, radius, shadows, layout props)
- Builds a reusable starter output:
  - index.html (structural clone starter)
  - ui-system.css (tokenized style baseline)
  - ui-report.md (analysis report)

Important:
- Use only on sites you own or have permission to analyze.
- This tool is for design-system replication workflows, not asset theft.
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys
import textwrap
import urllib.parse
import urllib.request


UA = "Mozilla/5.0 (compatible; WebsiteUICloner/1.0; +https://local-tool)"


def fetch_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        raw = resp.read()
    return raw.decode(charset, errors="replace")


def extract_stylesheet_links(html: str, base_url: str) -> list[str]:
    links: list[str] = []
    for m in re.finditer(
        r"""<link\b[^>]*rel=["'][^"']*stylesheet[^"']*["'][^>]*href=["']([^"']+)["'][^>]*>""",
        html,
        flags=re.IGNORECASE,
    ):
        href = m.group(1).strip()
        if not href:
            continue
        abs_url = urllib.parse.urljoin(base_url, href)
        if abs_url.startswith("http"):
            links.append(abs_url)
    # keep order, remove duplicates
    return list(dict.fromkeys(links))


def extract_inline_css(html: str) -> str:
    chunks: list[str] = []
    for m in re.finditer(
        r"<style\b[^>]*>(.*?)</style>", html, flags=re.IGNORECASE | re.DOTALL
    ):
        chunks.append(m.group(1))
    return "\n\n".join(chunks)


def strip_scripts(html: str) -> str:
    return re.sub(
        r"<script\b[^>]*>.*?</script>",
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


def extract_body_inner(html: str) -> str:
    m = re.search(r"<body\b[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return "<main><!-- body not detected --></main>"
    inner = m.group(1)
    inner = strip_scripts(inner)
    return inner.strip()


def normalize_css(css: str) -> str:
    # remove comments
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    return css


def parse_declarations(css: str) -> list[tuple[str, str]]:
    css = normalize_css(css)
    decls: list[tuple[str, str]] = []
    for prop, value in re.findall(r"([a-zA-Z-]+)\s*:\s*([^;{}]+);", css):
        decls.append((prop.strip().lower(), value.strip()))
    return decls


COLOR_RE = re.compile(
    r"(#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\))", flags=re.IGNORECASE
)
SIZE_RE = re.compile(r"(-?\d*\.?\d+(?:px|rem|em|vw|vh|%)|clamp\([^)]*\))")


def collect_style_signals(
    decls: list[tuple[str, str]]
) -> dict[str, collections.Counter[str]]:
    signals: dict[str, collections.Counter[str]] = {
        "colors": collections.Counter(),
        "font_family": collections.Counter(),
        "font_size": collections.Counter(),
        "spacing": collections.Counter(),
        "radius": collections.Counter(),
        "shadow": collections.Counter(),
        "layout": collections.Counter(),
        "timing": collections.Counter(),
    }

    spacing_props = {
        "margin",
        "margin-top",
        "margin-right",
        "margin-bottom",
        "margin-left",
        "padding",
        "padding-top",
        "padding-right",
        "padding-bottom",
        "padding-left",
        "gap",
        "row-gap",
        "column-gap",
    }
    layout_props = {
        "display",
        "grid-template-columns",
        "grid-template-rows",
        "align-items",
        "justify-content",
        "flex-direction",
        "position",
    }

    for prop, value in decls:
        for color in COLOR_RE.findall(value):
            signals["colors"][color.strip()] += 1

        if prop == "font-family":
            signals["font_family"][value] += 1
        if prop == "font-size":
            signals["font_size"][value] += 1
        if prop in spacing_props:
            signals["spacing"][value] += 1
            for token in SIZE_RE.findall(value):
                signals["spacing"][token.strip()] += 1
        if "radius" in prop:
            signals["radius"][value] += 1
        if "shadow" in prop:
            signals["shadow"][value] += 1
        if prop in layout_props:
            signals["layout"][f"{prop}: {value}"] += 1
        if prop in {"transition", "animation", "transition-duration", "animation-duration"}:
            signals["timing"][value] += 1

    return signals


def top_items(counter: collections.Counter[str], n: int = 10) -> list[str]:
    return [k for k, _ in counter.most_common(n)]


def build_token_css(signals: dict[str, collections.Counter[str]]) -> str:
    colors = top_items(signals["colors"], 8)
    radii = top_items(signals["radius"], 4)
    spacing = top_items(signals["spacing"], 8)
    shadows = top_items(signals["shadow"], 3)
    fonts = top_items(signals["font_family"], 1)
    font_sizes = top_items(signals["font_size"], 4)

    def fallback(lst: list[str], idx: int, default: str) -> str:
        return lst[idx] if idx < len(lst) else default

    return textwrap.dedent(
        f"""\
        /* Generated by website_ui_cloner.py */
        :root {{
          --c-bg: {fallback(colors, 0, "#f6f6f6")};
          --c-surface: {fallback(colors, 1, "#ffffff")};
          --c-text: {fallback(colors, 2, "#111111")};
          --c-muted: {fallback(colors, 3, "rgba(0,0,0,0.6)")};
          --c-line: {fallback(colors, 4, "rgba(0,0,0,0.12)")};
          --c-accent: {fallback(colors, 5, "#111111")};

          --radius-sm: {fallback(radii, 0, "8px")};
          --radius-md: {fallback(radii, 1, "14px")};
          --radius-lg: {fallback(radii, 2, "20px")};
          --radius-xl: {fallback(radii, 3, "28px")};

          --space-1: {fallback(spacing, 0, "8px")};
          --space-2: {fallback(spacing, 1, "12px")};
          --space-3: {fallback(spacing, 2, "16px")};
          --space-4: {fallback(spacing, 3, "24px")};
          --space-5: {fallback(spacing, 4, "32px")};

          --shadow-1: {fallback(shadows, 0, "0 12px 24px rgba(0,0,0,0.08)")};
          --shadow-2: {fallback(shadows, 1, "0 20px 40px rgba(0,0,0,0.12)")};
          --font-sans: {fallback(fonts, 0, "Inter, system-ui, -apple-system, sans-serif")};
          --fs-1: {fallback(font_sizes, 0, "13px")};
          --fs-2: {fallback(font_sizes, 1, "15px")};
          --fs-3: {fallback(font_sizes, 2, "20px")};
          --fs-4: {fallback(font_sizes, 3, "32px")};
        }}

        * {{ box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{
          margin: 0;
          font-family: var(--font-sans);
          color: var(--c-text);
          background: var(--c-bg);
          font-size: var(--fs-2);
          line-height: 1.5;
        }}

        .page {{
          width: min(1280px, calc(100% - 2 * var(--space-4)));
          margin: 0 auto;
          padding: var(--space-4) 0;
        }}

        .panel {{
          background: var(--c-surface);
          border: 1px solid var(--c-line);
          border-radius: var(--radius-lg);
          box-shadow: var(--shadow-1);
          padding: var(--space-4);
        }}

        .button {{
          display: inline-flex;
          align-items: center;
          justify-content: center;
          min-height: 44px;
          padding: 0 var(--space-3);
          border-radius: 999px;
          background: var(--c-accent);
          color: #fff;
          border: 1px solid transparent;
          text-decoration: none;
        }}

        .section {{
          margin-bottom: var(--space-5);
        }}

        @media (max-width: 1080px) {{
          .page {{
            width: calc(100% - 2 * var(--space-3));
          }}
        }}

        @media (max-width: 560px) {{
          .page {{
            width: calc(100% - 2 * var(--space-2));
          }}
        }}
        """
    ).strip() + "\n"


def heading_outline(html: str) -> list[str]:
    lines: list[str] = []
    for m in re.finditer(
        r"<h([1-6])\b[^>]*>(.*?)</h\1>", html, flags=re.IGNORECASE | re.DOTALL
    ):
        level = int(m.group(1))
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if text:
            lines.append(f'{"  " * (level - 1)}- h{level}: {text}')
    return lines


def build_index_html(body_inner: str, source_url: str) -> str:
    return textwrap.dedent(
        f"""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
          <meta name="color-scheme" content="light" />
          <title>Cloned UI Starter</title>
          <meta name="description" content="Generated UI starter cloned from visual/structural signals." />
          <link rel="stylesheet" href="./ui-system.css" />
        </head>
        <body>
          <!-- Source analyzed: {source_url} -->
          <div class="page">
            <!-- START: Structural clone (scripts removed intentionally) -->
        {indent_block(body_inner, 4)}
            <!-- END: Structural clone -->
          </div>
          <script>
            // Add your project interactions here.
          </script>
        </body>
        </html>
        """
    ).strip() + "\n"


def indent_block(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join((pad + line) if line else "" for line in text.splitlines())


def build_report(
    source_url: str,
    css_urls: list[str],
    signals: dict[str, collections.Counter[str]],
    html: str,
) -> str:
    outline = heading_outline(html)
    report = [
        "# UI Clone Report",
        "",
        f"- Source URL: `{source_url}`",
        f"- Stylesheets analyzed: `{len(css_urls)}`",
        "",
        "## Top Colors",
    ]
    report += [f"- `{item}`" for item in top_items(signals["colors"], 12)] or ["- none detected"]
    report += ["", "## Font Families"]
    report += [f"- `{item}`" for item in top_items(signals["font_family"], 6)] or ["- none detected"]
    report += ["", "## Font Sizes"]
    report += [f"- `{item}`" for item in top_items(signals["font_size"], 10)] or ["- none detected"]
    report += ["", "## Spacing Values"]
    report += [f"- `{item}`" for item in top_items(signals["spacing"], 12)] or ["- none detected"]
    report += ["", "## Radius Values"]
    report += [f"- `{item}`" for item in top_items(signals["radius"], 8)] or ["- none detected"]
    report += ["", "## Shadows"]
    report += [f"- `{item}`" for item in top_items(signals["shadow"], 8)] or ["- none detected"]
    report += ["", "## Layout Hints"]
    report += [f"- `{item}`" for item in top_items(signals["layout"], 12)] or ["- none detected"]
    report += ["", "## Heading Outline"]
    report += outline or ["- no headings detected"]
    report += [
        "",
        "## Notes",
        "- This output is a design-system starter, not a binary-perfect source clone.",
        "- Dynamic behavior (framework code, API data, auth flows) is intentionally not replicated.",
        "- Replace content/assets with licensed equivalents before production use.",
    ]
    return "\n".join(report).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze website UI and generate reusable clone starter files."
    )
    parser.add_argument("url", help="Target URL to analyze")
    parser.add_argument(
        "-o",
        "--output",
        default="ui-clone-output",
        help="Output directory (default: ui-clone-output)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="HTTP timeout seconds (default: 20)",
    )
    args = parser.parse_args()

    source_url = args.url.strip()
    if not source_url.startswith(("http://", "https://")):
        print("Error: URL must start with http:// or https://", file=sys.stderr)
        return 2

    out_dir = pathlib.Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] Fetching HTML: {source_url}")
    html = fetch_text(source_url, timeout=args.timeout)

    print("[2/4] Collecting CSS sources")
    css_links = extract_stylesheet_links(html, source_url)
    inline_css = extract_inline_css(html)
    all_css_parts = [inline_css] if inline_css else []

    for css_url in css_links:
        try:
            all_css_parts.append(fetch_text(css_url, timeout=args.timeout))
        except Exception as exc:  # noqa: BLE001
            print(f"  - warning: failed CSS fetch {css_url}: {exc}", file=sys.stderr)

    all_css = "\n\n".join(all_css_parts)
    decls = parse_declarations(all_css)
    signals = collect_style_signals(decls)

    print("[3/4] Generating output files")
    body_inner = extract_body_inner(html)
    index_html = build_index_html(body_inner, source_url)
    ui_css = build_token_css(signals)
    report = build_report(source_url, css_links, signals, html)

    (out_dir / "index.html").write_text(index_html, encoding="utf-8")
    (out_dir / "ui-system.css").write_text(ui_css, encoding="utf-8")
    (out_dir / "ui-report.md").write_text(report, encoding="utf-8")

    print("[4/4] Done")
    print(f"- Output: {out_dir}")
    print(f"- Files: index.html, ui-system.css, ui-report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
