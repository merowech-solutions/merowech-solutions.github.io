#!/usr/bin/env python3
"""Zero-dependency static Insights, RSS, and Sitemap generator for Merowech Solutions.

Uses only the Python 3 standard library (compatible with Python 3.9+).
Reads Markdown files in `content/insights/{en,de}/*.md` and generates:
  - /en/insights/<slug>/index.html & /de/insights/<slug>/index.html
  - /en/insights/index.html & /de/insights/index.html
  - /en/insights/rss.xml & /de/insights/rss.xml
  - /sitemap.xml
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://merowech-solutions.de"


def slugify(text: str) -> str:
    s = text.lower()
    s = (
        s.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"


def parse_frontmatter(raw: str) -> Tuple[Dict[str, str], str]:
    if not raw.startswith("---\n"):
        raise ValueError("Markdown file must begin with YAML-style '---' frontmatter.")
    end = raw.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Unclosed frontmatter block.")
    fm_block = raw[4:end]
    body = raw[end + 5 :].strip()
    meta: Dict[str, str] = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def _format_link(match: re.Match[str]) -> str:
    label = match.group(1)
    href_raw = match.group(2)
    href = html.escape(href_raw, quote=True)
    if href_raw.startswith(("http://", "https://")) and not href_raw.startswith(ORIGIN):
        return f'<a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>'
    return f'<a href="{href}">{label}</a>'


def render_inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    # Inline code
    escaped = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", escaped)
    # Links [label](href)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _format_link, escaped)
    # Bold & italic
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def render_markdown(md: str) -> Tuple[str, List[Tuple[str, str]]]:
    lines = md.splitlines()
    out: List[str] = []
    toc: List[Tuple[str, str]] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            i += 1
            code_lines: List[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code_escaped = html.escape("\n".join(code_lines))
            out.append(f"<pre><code>{code_escaped}</code></pre>")
            continue

        # Callout block :::callout Title
        if stripped.startswith(":::callout"):
            title = stripped[len(":::callout") :].strip()
            i += 1
            c_lines: List[str] = []
            while i < n and lines[i].strip() != ":::":
                c_lines.append(lines[i].strip())
                i += 1
            i += 1
            c_body = render_inline(" ".join(x for x in c_lines if x))
            title_html = (
                f'<span class="callout-title">{html.escape(title)}</span>' if title else ""
            )
            out.append(f'<aside class="callout">{title_html}<p>{c_body}</p></aside>')
            continue

        # Headings
        if stripped.startswith("## "):
            h_text = stripped[3:].strip()
            h_id = slugify(h_text)
            toc.append((h_id, h_text))
            out.append(f'<h2 id="{h_id}">{render_inline(h_text)}</h2>')
            i += 1
            continue

        if stripped.startswith("### "):
            h_text = stripped[4:].strip()
            h_id = slugify(h_text)
            out.append(f'<h3 id="{h_id}">{render_inline(h_text)}</h3>')
            i += 1
            continue

        # Markdown Table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s\-:|]+\|\s*$", lines[i + 1]):
            headers = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # skip header + separator
            rows: List[List[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th_html = "".join(f"<th>{render_inline(h)}</th>" for h in headers)
            trs_html = "".join(
                "<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in r) + "</tr>"
                for r in rows
            )
            out.append(f"<table><thead><tr>{th_html}</tr></thead><tbody>{trs_html}</tbody></table>")
            continue

        # Unordered list
        if stripped.startswith("- "):
            items: List[str] = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(f"<li>{render_inline(lines[i].strip()[2:].strip())}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item_txt = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append(f"<li>{render_inline(item_txt)}</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue

        # Paragraph
        p_lines: List[str] = []
        while (
            i < n
            and lines[i].strip()
            and not lines[i].strip().startswith(("```", ":::callout", "## ", "### ", "- ", "|"))
            and not re.match(r"^\d+\.\s+", lines[i].strip())
        ):
            p_lines.append(lines[i].strip())
            i += 1
        out.append(f"<p>{render_inline(' '.join(p_lines))}</p>")

    return "\n".join(out), toc


def render_article_page(lang: str, meta: Dict[str, str], body_html: str, toc: List[Tuple[str, str]]) -> str:
    is_de = lang == "de"
    slug = meta["slug"]
    alt_slug = meta["alt_slug"]

    en_url = f"{ORIGIN}/en/insights/{slug if not is_de else alt_slug}/"
    de_url = f"{ORIGIN}/de/insights/{slug if is_de else alt_slug}/"
    canonical = de_url if is_de else en_url

    back_href = "/de/insights/" if is_de else "/en/insights/"
    back_label = "← Alle Insights" if is_de else "← All Insights"
    toc_title = "INHALT" if is_de else "ON THIS PAGE"
    cta_kicker = "FACHLICHER AUSTAUSCH" if is_de else "TECHNICAL EXCHANGE"
    cta_title = (
        "Sie arbeiten an einer ähnlichen Fragestellung?"
        if is_de
        else "Working on a related machine learning or XAI challenge?"
    )
    cta_body = (
        "Schreiben Sie uns direkt per E-Mail oder vernetzen Sie sich auf LinkedIn für ein unverbindliches Fachgespräch."
        if is_de
        else "Reach out directly via email or connect on LinkedIn for a straightforward technical discussion."
    )
    copy_label = "E-Mail kopieren" if is_de else "Copy email"

    toc_items = "\n".join(
        f'<li><a href="#{h_id}" class="{"is-active" if idx == 0 else ""}">{html.escape(h_txt)}</a></li>'
        for idx, (h_id, h_txt) in enumerate(toc)
    )

    ld_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": meta["title"],
            "description": meta["subtitle"],
            "datePublished": meta["date"],
            "inLanguage": lang,
            "author": {
                "@type": "Organization",
                "name": "Merowech Solutions",
                "url": ORIGIN,
            },
            "publisher": {
                "@type": "Organization",
                "name": "Merowech Solutions",
                "url": ORIGIN,
            },
            "mainEntityOfPage": canonical,
        },
        ensure_ascii=False,
        indent=2,
    )

    title_esc = html.escape(meta["title"])
    sub_esc = html.escape(meta["subtitle"])
    meta_line = f'{html.escape(meta["date_label"])}  ·  {html.escape(meta["read_time"])}  ·  {html.escape(meta["topic"])}'

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title_esc} — Merowech Solutions</title>
  <meta name="description" content="{sub_esc}" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="en" href="{en_url}" />
  <link rel="alternate" hreflang="de" href="{de_url}" />
  <link rel="alternate" hreflang="x-default" href="{en_url}" />

  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Merowech Solutions" />
  <meta property="og:title" content="{title_esc}" />
  <meta property="og:description" content="{sub_esc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{ORIGIN}/assets/img/og-card.svg" />

  <script src="/assets/js/theme-init.js"></script>
  <link rel="stylesheet" href="/assets/css/tokens.css" />
  <link rel="stylesheet" href="/assets/css/base.css" />
  <link rel="stylesheet" href="/assets/css/layout.css" />
  <link rel="stylesheet" href="/assets/css/components.css" />

  <script type="application/ld+json">
{ld_json}
  </script>
</head>
<body>
  <site-header></site-header>

  <main id="main-content" class="container">
    <section class="page-header">
      <div class="mb-6">
        <a href="{back_href}" class="card-cta" style="margin-top:0;">{back_label}</a>
      </div>
      <div class="kicker">{meta_line}</div>
      <h1 class="page-title" style="max-width:28ch;">{title_esc}</h1>
      <p class="lead">{sub_esc}</p>
    </section>

    <section class="section">
      <div class="article-layout">
        <article class="prose">
{body_html}
        </article>

        <aside class="sticky-rail">
          <div class="toc-box">
            <div class="toc-title">{toc_title}</div>
            <ul class="toc-list">
{toc_items}
            </ul>
          </div>
        </aside>
      </div>
    </section>

    <section class="section-last">
      <div class="cta-panel">
        <div style="max-width:38rem;">
          <div class="kicker" style="margin-bottom:0.55rem;">{cta_kicker}</div>
          <h2 class="section-title mb-2">{cta_title}</h2>
          <p class="card-body">{cta_body}</p>
        </div>
        <div class="cta-actions">
          <div class="cta-email-group">
            <a href="mailto:contact@merowech-solutions.de" class="btn btn-primary btn-mono">contact@merowech-solutions.de</a>
            <button type="button" class="btn btn-secondary btn-mono" data-copy-email>{copy_label}</button>
          </div>
          <a href="https://www.linkedin.com/in/udo-schlegel/" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-mono">linkedin.com/in/udo-schlegel ↗</a>
        </div>
      </div>
    </section>
  </main>

  <site-footer></site-footer>
  <script type="module" src="/assets/js/main.js"></script>
</body>
</html>
"""


def render_insights_index(lang: str, posts: List[Dict[str, str]]) -> str:
    is_de = lang == "de"
    en_url = f"{ORIGIN}/en/insights/"
    de_url = f"{ORIGIN}/de/insights/"
    canonical = de_url if is_de else en_url
    rss_href = f"/{lang}/insights/rss.xml"

    title = (
        "Insights & Fachbeiträge — Merowech Solutions"
        if is_de
        else "Insights & Technical Essays — Merowech Solutions"
    )
    desc = (
        "Fachbeiträge aus Forschung und Praxis zu Machine Learning, Data Science, Explainable AI (XAI), Zeitreihenanalyse und GenAI."
        if is_de
        else "Notes and technical deep-dives from research and applied practice on Machine Learning, Data Science, Explainable AI (XAI), Time Series, and GenAI."
    )
    kicker = "INSIGHTS & PUBLIKATIONEN" if is_de else "INSIGHTS & PUBLICATIONS"
    h1 = (
        "Methodische Notizen aus Machine Learning, Data Science & Explainable AI."
        if is_de
        else "Methodological notes from Machine Learning, Data Science & Explainable AI."
    )

    filters = (
        [
            ("all", "Alle"),
            ("Machine Learning", "Machine Learning"),
            ("Data Science", "Data Science"),
            ("Explainable AI", "Explainable AI"),
            ("Time Series", "Zeitreihen"),
            ("GenAI", "GenAI & Evals"),
        ]
        if is_de
        else [
            ("all", "All"),
            ("Machine Learning", "Machine Learning"),
            ("Data Science", "Data Science"),
            ("Explainable AI", "Explainable AI"),
            ("Time Series", "Time Series"),
            ("GenAI", "GenAI & Evals"),
        ]
    )

    pills_html = "\n".join(
        f'<button type="button" class="pill{" is-active" if idx == 0 else ""}" data-filter-tag="{tag}" aria-pressed="{"true" if idx == 0 else "false"}">{label}</button>'
        for idx, (tag, label) in enumerate(filters)
    )

    rows_html = "\n".join(
        f"""        <a href="/{lang}/insights/{p['slug']}/" class="insight-row" data-post-tags="{html.escape(p['tags'])}">
          <div>
            <span class="insight-row-topic">{html.escape(p['topic'])}</span>
            <h2 class="insight-row-title">{html.escape(p['title'])}</h2>
            <p class="insight-row-summary">{html.escape(p['subtitle'])}</p>
          </div>
          <span class="insight-row-meta">{html.escape(p['date_label'])} · {html.escape(p['read_time'])}</span>
        </a>"""
        for p in posts
    )

    rss_label = "RSS-Feed abonnieren ↗" if is_de else "Subscribe via RSS ↗"

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="en" href="{en_url}" />
  <link rel="alternate" hreflang="de" href="{de_url}" />
  <link rel="alternate" hreflang="x-default" href="{en_url}" />
  <link rel="alternate" type="application/rss+xml" title="{html.escape(title)}" href="{rss_href}" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{ORIGIN}/assets/img/og-card.svg" />

  <script src="/assets/js/theme-init.js"></script>
  <link rel="stylesheet" href="/assets/css/tokens.css" />
  <link rel="stylesheet" href="/assets/css/base.css" />
  <link rel="stylesheet" href="/assets/css/layout.css" />
  <link rel="stylesheet" href="/assets/css/components.css" />
</head>
<body>
  <site-header></site-header>

  <main id="main-content" class="container">
    <section class="page-header">
      <div class="kicker">{kicker}</div>
      <h1 class="page-title">{html.escape(h1)}</h1>
      <p class="lead">{html.escape(desc)}</p>
    </section>

    <section class="section-last">
      <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem;" class="mb-6">
        <div class="filter-bar" style="margin-bottom:0;" role="toolbar" aria-label="Topic filter">
{pills_html}
        </div>
        <a href="{rss_href}" class="card-cta" style="margin-top:0;">{rss_label}</a>
      </div>

      <div class="insight-list">
{rows_html}
      </div>
    </section>
  </main>

  <site-footer></site-footer>
  <script type="module" src="/assets/js/main.js"></script>
</body>
</html>
"""


def render_rss(lang: str, posts: List[Dict[str, str]]) -> str:
    is_de = lang == "de"
    title = (
        "Merowech Solutions — Insights (Deutsch)"
        if is_de
        else "Merowech Solutions — Insights (English)"
    )
    desc = (
        "Fachbeiträge zu Data Science, Machine Learning und Explainable AI."
        if is_de
        else "Technical essays on Data Science, Machine Learning, and Explainable AI."
    )
    items = []
    for p in posts:
        url = f"{ORIGIN}/{lang}/insights/{p['slug']}/"
        pub_dt = dt.datetime.strptime(p["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 09:00:00 +0100")
        items.append(
            f"""    <item>
      <title>{xml_escape(p['title'])}</title>
      <link>{url}</link>
      <guid>{url}</guid>
      <pubDate>{pub_dt}</pubDate>
      <description>{xml_escape(p['subtitle'])}</description>
    </item>"""
        )

    items_xml = "\n".join(items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{xml_escape(title)}</title>
    <link>{ORIGIN}/{lang}/insights/</link>
    <description>{xml_escape(desc)}</description>
    <language>{lang}</language>
{items_xml}
  </channel>
</rss>
"""


def build_sitemap(en_posts: List[Dict[str, str]], de_posts: List[Dict[str, str]]) -> str:
    today = dt.date.today().isoformat()
    static_pairs = [
        ("/en/", "/de/"),
        ("/en/services/machine-learning/", "/de/leistungen/machine-learning/"),
        ("/en/services/explainable-ai/", "/de/leistungen/explainable-ai/"),
        ("/en/services/ai-strategy/", "/de/leistungen/ki-strategie/"),
        ("/en/services/genai-systems/", "/de/leistungen/genai-systeme/"),
        ("/en/insights/", "/de/insights/"),
        ("/en/about/", "/de/ueber-uns/"),
        ("/en/contact/", "/de/kontakt/"),
    ]

    entries: List[str] = [
        f"""  <url>
    <loc>{ORIGIN}/</loc>
    <lastmod>{today}</lastmod>
  </url>"""
    ]

    for en_p, de_p in static_pairs:
        for loc in (en_p, de_p):
            entries.append(
                f"""  <url>
    <loc>{ORIGIN}{loc}</loc>
    <lastmod>{today}</lastmod>
  </url>"""
            )

    for p in en_posts:
        entries.append(
            f"""  <url>
    <loc>{ORIGIN}/en/insights/{p['slug']}/</loc>
    <lastmod>{p['date']}</lastmod>
  </url>"""
        )

    for p in de_posts:
        entries.append(
            f"""  <url>
    <loc>{ORIGIN}/de/insights/{p['slug']}/</loc>
    <lastmod>{p['date']}</lastmod>
  </url>"""
        )

    urls_xml = "\n".join(entries)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_xml}
</urlset>
"""


def process_language(lang: str) -> List[Dict[str, str]]:
    src_dir = ROOT / "content" / "insights" / lang
    out_base = ROOT / lang / "insights"
    out_base.mkdir(parents=True, exist_ok=True)

    posts: List[Dict[str, str]] = []
    for md_file in sorted(src_dir.glob("*.md")):
        raw = md_file.read_text(encoding="utf-8")
        meta, md_body = parse_frontmatter(raw)
        body_html, toc = render_markdown(md_body)
        article_html = render_article_page(lang, meta, body_html, toc)

        article_dir = out_base / meta["slug"]
        article_dir.mkdir(parents=True, exist_ok=True)
        (article_dir / "index.html").write_text(article_html, encoding="utf-8")
        posts.append(meta)

    posts.sort(key=lambda p: p["date"], reverse=True)
    active_slugs = {p["slug"] for p in posts}
    for child in out_base.iterdir():
        if child.is_dir() and child.name not in active_slugs:
            shutil.rmtree(child)

    (out_base / "index.html").write_text(render_insights_index(lang, posts), encoding="utf-8")
    (out_base / "rss.xml").write_text(render_rss(lang, posts), encoding="utf-8")
    return posts


def main() -> None:
    en_posts = process_language("en")
    de_posts = process_language("de")
    sitemap_xml = build_sitemap(en_posts, de_posts)
    (ROOT / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    print(f"Built {len(en_posts)} EN essays, {len(de_posts)} DE essays, RSS feeds, and sitemap.xml.")


if __name__ == "__main__":
    main()
