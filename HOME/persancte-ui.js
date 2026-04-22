/*
  PERSANCTE UI INTERACTIONS
  Version: 1.0
  Dependency: none (vanilla JS)

  Provides:
  - Dynamic header height -> CSS vars (--header-height, --scroll-offset)
  - Viewport/orientation data attributes on <html>
  - Mobile nav toggle (aria-safe)
  - Header hide-on-scroll-down/show-on-scroll-up
  - Scrollspy for section links (aria-current)
  - Internal-link prefetch on intent events
*/

(function persancteUiBootstrap() {
  const root = document.documentElement;

  /* ---------------------------
     1) Dynamic header metrics
     --------------------------- */
  const siteHeader = document.querySelector(".site-header");
  const updateHeaderHeight = () => {
    if (!siteHeader) return;
    const rect = siteHeader.getBoundingClientRect();
    const offset = Math.round(rect.height + 20);
    root.style.setProperty("--header-height", rect.height + "px");
    root.style.setProperty("--scroll-offset", offset + "px");
  };
  updateHeaderHeight();

  if ("ResizeObserver" in window && siteHeader) {
    new ResizeObserver(updateHeaderHeight).observe(siteHeader);
  } else {
    window.addEventListener("resize", updateHeaderHeight, { passive: true });
  }
  window.addEventListener("orientationchange", updateHeaderHeight);
  window.addEventListener("load", updateHeaderHeight);

  /* ---------------------------
     2) Viewport state flags
     --------------------------- */
  const applyViewportFlags = () => {
    const w = window.innerWidth;
    const h = window.innerHeight;
    let size = "desktop";
    if (w < 380) size = "xs";
    else if (w < 560) size = "sm";
    else if (w < 820) size = "md";
    else if (w < 1080) size = "lg";
    else if (w < 1680) size = "xl";
    else size = "2xl";

    root.dataset.viewport = size;
    root.dataset.orientation = w >= h ? "landscape" : "portrait";
  };
  applyViewportFlags();
  window.addEventListener("resize", applyViewportFlags, { passive: true });
  window.addEventListener("orientationchange", applyViewportFlags);

  /* ---------------------------
     3) Mobile nav
     --------------------------- */
  const headerShell = document.querySelector(".header-shell");
  const navToggle = document.querySelector(".nav-toggle");
  const primaryNav = document.getElementById("primary-nav");
  const mainEl = document.getElementById("main");
  const siteFooter = document.querySelector(".site-footer");

  const setNavOpen = (open) => {
    if (!headerShell || !navToggle) return;
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    headerShell.setAttribute("data-nav-open", open ? "true" : "false");
    if (open) {
      document.body.setAttribute("data-nav-open", "true");
    } else {
      document.body.removeAttribute("data-nav-open");
    }
    if (mainEl) {
      try {
        mainEl.inert = open;
      } catch (_) {
        /* inert unsupported */
      }
    }
    if (siteFooter) {
      try {
        siteFooter.inert = open;
      } catch (_) {
        /* inert unsupported */
      }
    }
  };

  if (navToggle && headerShell) {
    setNavOpen(false);
    navToggle.addEventListener("click", () => {
      const isOpen = navToggle.getAttribute("aria-expanded") === "true";
      setNavOpen(!isOpen);
    });
  }

  if (primaryNav) {
    primaryNav.addEventListener("click", (event) => {
      const target = event.target;
      if (target && target.closest && target.closest("a")) {
        setNavOpen(false);
      }
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navToggle?.getAttribute("aria-expanded") === "true") {
      setNavOpen(false);
      navToggle.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (!headerShell || headerShell.getAttribute("data-nav-open") !== "true") return;
    if (!headerShell.contains(event.target)) setNavOpen(false);
  });

  const desktopNav = window.matchMedia("(min-width: 821px)");
  const handleBreakpoint = (e) => {
    if (e.matches) setNavOpen(false);
  };
  if (desktopNav.addEventListener) {
    desktopNav.addEventListener("change", handleBreakpoint);
  } else if (desktopNav.addListener) {
    desktopNav.addListener(handleBreakpoint);
  }

  /* ---------------------------
     4) Header hide-on-scroll
     --------------------------- */
  if (siteHeader) {
    let lastY = window.scrollY;
    let ticking = false;
    const THRESHOLD = 8;
    const SHOW_ABOVE = 80;

    const reduceMotion =
      window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const updateHeaderVisibility = () => {
      const y = window.scrollY;
      const delta = y - lastY;

      if (reduceMotion) {
        siteHeader.setAttribute("data-hidden", "false");
        lastY = y;
        ticking = false;
        return;
      }

      if (y < SHOW_ABOVE) {
        siteHeader.setAttribute("data-hidden", "false");
      } else if (Math.abs(delta) > THRESHOLD) {
        const navOpen = headerShell?.getAttribute("data-nav-open") === "true";
        if (delta > 0 && !navOpen) {
          siteHeader.setAttribute("data-hidden", "true");
        } else {
          siteHeader.setAttribute("data-hidden", "false");
        }
      }

      lastY = y;
      ticking = false;
    };

    window.addEventListener(
      "scroll",
      () => {
        if (!ticking) {
          requestAnimationFrame(updateHeaderVisibility);
          ticking = true;
        }
      },
      { passive: true }
    );
  }

  /* ---------------------------
     5) Internal-link prefetch
     --------------------------- */
  const prefetched = new Set();

  const isPrefetchEligible = (href) => {
    if (!href) return false;
    if (href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("tel:")) return false;
    try {
      const url = new URL(href, window.location.href);
      return url.origin === window.location.origin;
    } catch (_) {
      return false;
    }
  };

  const prefetch = (href) => {
    if (!isPrefetchEligible(href) || prefetched.has(href)) return;
    const link = document.createElement("link");
    link.rel = "prefetch";
    link.href = href;
    document.head.appendChild(link);
    prefetched.add(href);
  };

  document.querySelectorAll("a[href]").forEach((anchor) => {
    const href = anchor.getAttribute("href");
    const trigger = () => prefetch(href);
    anchor.addEventListener("pointerenter", trigger, { once: true, passive: true });
    anchor.addEventListener("touchstart", trigger, { once: true, passive: true });
    anchor.addEventListener("focus", trigger, { once: true });
  });

  /* ---------------------------
     6) Scrollspy
     --------------------------- */
  const navLinks = Array.from(document.querySelectorAll("[data-nav]"));
  const sectionIds = ["top", "work", "capabilities", "systems", "contact"];
  const sections = sectionIds
    .map((id) => document.getElementById(id))
    .filter(Boolean);

  const setActiveNav = (id) => {
    navLinks.forEach((link) => {
      const isActive = link.dataset.nav === id;
      if (isActive) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  };

  const applyHashToNav = () => {
    const raw = (location.hash || "#top").replace(/^#/, "");
    const id = raw === "" ? "top" : raw;
    if (sectionIds.includes(id)) {
      setActiveNav(id);
    } else if (!location.hash) {
      setActiveNav("top");
    }
  };

  if (sections.length) {
    setActiveNav("top");
    applyHashToNav();
    window.addEventListener("hashchange", applyHashToNav, { passive: true });
    window.addEventListener(
      "load",
      () => {
        requestAnimationFrame(applyHashToNav);
      },
      { once: true }
    );

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          const visible = entries
            .filter((entry) => entry.isIntersecting)
            .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

          if (visible?.target?.id) {
            setActiveNav(visible.target.id);
          }
        },
        {
          rootMargin: "-32% 0px -42% 0px",
          threshold: [0, 0.01, 0.05, 0.1]
        }
      );

      sections.forEach((section) => observer.observe(section));
    }
  }

  /* ---------------------------
     7) Custom pointer cursor (replaces system cursor; disabled on touch / reduced motion)
     --------------------------- */
  (function initCustomCursor() {
    if (typeof document === "undefined" || !document.querySelector) return;
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const el = document.createElement("div");
    el.className = "ui-cursor";
    el.setAttribute("aria-hidden", "true");
    const dot = document.createElement("span");
    dot.className = "ui-cursor__dot";
    const ring = document.createElement("span");
    ring.className = "ui-cursor__ring";
    el.appendChild(dot);
    el.appendChild(ring);
    document.body.appendChild(el);
    document.documentElement.classList.add("has-ui-cursor");

    const pointerHintSelector =
      "a, button, input, textarea, select, label, summary, [role='button'], [data-cursor='pointer']";

    let raf = 0;
    let mx = 0;
    let my = 0;
    let lastHover = false;

    const flush = () => {
      raf = 0;
      el.style.left = `${mx}px`;
      el.style.top = `${my}px`;
      let isHover = false;
      const node = document.elementFromPoint(mx, my);
      if (node && node.nodeType === 1) {
        const t = node.closest(pointerHintSelector);
        isHover = Boolean(t);
      }
      if (isHover !== lastHover) {
        lastHover = isHover;
        el.classList.toggle("is-hover", isHover);
      }
    };

    const onMove = (e) => {
      mx = e.clientX;
      my = e.clientY;
      if (!el.classList.contains("is-active")) {
        el.classList.add("is-active");
      }
      if (raf) return;
      raf = requestAnimationFrame(flush);
    };

    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(flush);
    };
    document.addEventListener("mousemove", onMove, { passive: true });
    document.addEventListener("scroll", onScroll, { passive: true, capture: true });

    document.addEventListener(
      "mouseout",
      (e) => {
        if (e.relatedTarget != null) return;
        el.classList.remove("is-active", "is-hover");
        lastHover = false;
      },
      { passive: true }
    );
  })();
})();
