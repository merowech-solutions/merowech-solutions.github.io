# Merowech Solutions — `merowech-solutions.de`

![Merowech Solutions](./assets/img/logo-lockup.svg)

Zero-dependency, bilingual (**EN / DE**) static consulting website and technical publication for **Merowech Solutions** — focused on **Data Science**, **Machine Learning**, and **Explainable AI (XAI)** (including applied **Time-Series Analysis**, AI Strategy, and Verifiable GenAI / RAG).

## Architecture Highlights

- **Zero npm / Node build pipeline:** Deploys directly from `main` on GitHub Pages (`.nojekyll` + `CNAME` for `merowech-solutions.de`, while working identically on `merowech-solutions.github.io`).
- **DACH Privacy-by-Design:** 100% self-hosted variable `.woff2` fonts (`Manrope` & `JetBrains Mono`), zero cookies, zero external trackers, and direct email + LinkedIn contact flows.
- **Shared Chrome via Native Web Components:** `<site-header>` (`assets/js/site-header.js`) and `<site-footer>` (`assets/js/site-footer.js`) provide navigation, native `<dialog>` mobile drawer, `hreflang`-driven `EN / DE` switching, and warm light/dark mode from a single source of truth.
- **Optional Python 3 Stdlib Insights Generator:** Author technical essays in `content/insights/{en,de}/*.md` and compile static HTML pages, RSS feeds, and `sitemap.xml` with zero external packages.

## Local Preview

### Option A — Docker Compose (Nginx, mirrors GitHub Pages routing & `404.html`)

```sh
docker compose up -d
```

Then open `http://localhost:8080` (or override the port via `PORT=3000 docker compose up -d`).

### Option B — Python Built-In Server

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Publishing or Updating Insights Essays

1. Add or edit Markdown files in `content/insights/en/` and `content/insights/de/` (linking translations via `slug` and `alt_slug` in frontmatter).
2. Run the zero-dependency generator locally or via Docker Compose:

```sh
python3 scripts/build_insights.py
# or via Docker:
docker compose run --rm insights
```

This updates `/en/insights/`, `/de/insights/`, both `rss.xml` feeds, and `/sitemap.xml`.

## Pre-Launch Checklist

- **Contact email:** Update `email` in `assets/js/config.js` (and `mailto:` links if changing away from `contact@merowech-solutions.de`).
- **Legal disclosures (`§ 5 DDG` & `DSGVO`):** Replace the `[TODO: ...]` street address / postal city / VAT ID placeholders in:
  - `en/imprint/index.html` & `de/impressum/index.html`
  - `en/privacy/index.html` & `de/datenschutz/index.html`
