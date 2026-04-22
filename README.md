# WebsiteME

## View the site in a browser

On GitHub, **Code → `HOME/home.html`** shows the **HTML source** (syntax-highlighted). That is normal; it is not a live page preview.

To open the page **rendered**:

1. **Repository → Settings → Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions** (if prompted).
3. After the workflow **Deploy HOME to GitHub Pages** runs on `main`, open the **Visit site** URL from the workflow run or from **Settings → Pages** (typically `https://sancte3d.github.io/WebsiteME/`).

The published root redirects to `home.html`; assets stay in `HOME/` next to that file.

## Enable Pages from your PC (no clicking in Settings)

If you prefer a one-liner after creating a [Personal access token](https://github.com/settings/tokens) with **repo** access to this repository:

```powershell
cd $HOME\Desktop\WebsiteME
$env:GITHUB_TOKEN = "paste_token_here"
.\scripts\enable-github-pages.ps1
```

Then open **Actions** and wait for **Deploy HOME to GitHub Pages** to finish; the site URL appears under **Settings → Pages**.
