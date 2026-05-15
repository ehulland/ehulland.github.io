#!/usr/bin/env python3
import datetime
import html
import re
from pathlib import Path

import markdown
import requests
import yaml


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONFIG = ROOT / "_config.yml"
CSS_SRC = ROOT / "site.css"
ABOUT_QMD = ROOT / "about.qmd"
ABOUT_MD = ROOT / "_pages" / "about.md"
CV_QMD = ROOT / "cv.qmd"
POSTS = ROOT / "_posts"
PUBLICATIONS = ROOT / "_publications"
TALKS = ROOT / "_talks"
MAP_LABEL = "Timeline Map"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_site_config(path: Path):
  text = read_text(path)
  text = re.sub(r":\s*&[A-Za-z0-9_-]+\s+", ": ", text)
  text = re.sub(r"\*[A-Za-z0-9_-]+", "", text)
  return yaml.safe_load(text) or {}


def parse_frontmatter(path: Path):
    text = read_text(path)
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not match:
        return {}, text
    frontmatter = yaml.safe_load(match.group(1)) or {}
    body = match.group(2)
    return frontmatter, body


def as_date_str(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return str(value) if value is not None else ""


def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["extra", "sane_lists"])


def strip_liquid(text: str) -> str:
  text = re.sub(r"\{\%.*?\%\}", "", text, flags=re.S)
  text = re.sub(r"\{\{.*?\}\}", "", text, flags=re.S)
  return text


def first_existing(*paths: Path):
  for path in paths:
    if path.exists():
      return path
  return None


def remove_about_map_section(text: str) -> str:
  return re.sub(
      r"\n## Places I've Lived, Studied, and Worked.*?(?=\n## |\Z)",
      "\n",
      text,
      flags=re.S,
  ).strip() + "\n"


def resolve_avatar_path() -> str:
  docs_images = DOCS / "images"
  docs_images.mkdir(parents=True, exist_ok=True)
  candidates = [
    ROOT / "headshot_color.jpg",
    ROOT / "images" / "profile.png",
  ]
  src = first_existing(*candidates)
  if src is None:
    return "/images/profile.png"
  dest_name = "headshot-color" + src.suffix.lower()
  dest = docs_images / dest_name
  if src.resolve() != dest.resolve():
    dest.write_bytes(src.read_bytes())
  return f"/images/{dest_name}"


def page_shell(title: str, content: str, site_title: str):
    full_title = html.escape(site_title) if title == site_title else f"{html.escape(title)} | {html.escape(site_title)}"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <script>
    (function() {{
      var saved = localStorage.getItem("theme");
      var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      if (saved === "dark" || (!saved && prefersDark)) {{
        document.documentElement.setAttribute("data-theme", "dark");
      }}
    }})();
  </script>
  <link rel="stylesheet" href="/site.css">
</head>
<body>
  <nav class="navbar">
    <div class="wrap">
      <a class="brand" href="/">{html.escape(site_title)}</a>
      <a href="/about.html">About me</a>
      <a href="/publications.html">Publications</a>
      <a href="/talks.html">Talks and presentations</a>
      <a href="/talkmap/map.html">{MAP_LABEL}</a>
      <a href="/posts.html">Posts</a>
      <a href="/cv.html">CV</a>
      <button class="theme-toggle" onclick="(function(){{var h=document.documentElement;var dark=h.getAttribute('data-theme')==='dark';h.setAttribute('data-theme',dark?'light':'dark');localStorage.setItem('theme',dark?'light':'dark');}})()" aria-label="Toggle dark mode">
        <span class="icon-moon">&#9790;</span>
        <span class="icon-sun">&#9788;</span>
      </button>
    </div>
  </nav>
  {content}
</body>
</html>
'''


ICON_GITHUB = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
ICON_LINKEDIN = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
ICON_X = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>'
ICON_SCHOLAR = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M12 3L1 9l11 6 11-6-11-6zM5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/></svg>'

def render_home(site_title, author, avatar):
    name = author.get("name", "")
    bio = author.get("bio", "")
    location = author.get("location", "")
    github = author.get("github", "")
    linkedin = author.get("linkedin", "")
    twitter = author.get("twitter", "")
    googlescholar = author.get("googlescholar", "")
    social = []
    if github:
        social.append(f'<a class="social-icon" href="https://github.com/{html.escape(github)}" aria-label="GitHub" title="GitHub">{ICON_GITHUB}</a>')
    if linkedin:
        social.append(f'<a class="social-icon" href="https://www.linkedin.com/in/{html.escape(linkedin)}" aria-label="LinkedIn" title="LinkedIn">{ICON_LINKEDIN}</a>')
    if twitter:
        social.append(f'<a class="social-icon" href="https://x.com/{html.escape(twitter)}" aria-label="X (Twitter)" title="X (Twitter)">{ICON_X}</a>')
    if googlescholar:
        social.append(f'<a class="social-icon" href="{html.escape(googlescholar)}" aria-label="Google Scholar" title="Google Scholar">{ICON_SCHOLAR}</a>')
    social_html = '<div class="social-icons">' + "".join(social) + '</div>' if social else ""

    content = f'''
  <section class="hero hero-profile">
    <div class="container hero-grid">
      <div>
        <h1>{html.escape(name)}</h1>
        <p class="lead">{html.escape(bio)}</p>
        <p><strong>Location:</strong> {html.escape(location)}</p>
        {social_html}
        <p><a class="button" href="/about.html">Learn more</a></p>
      </div>
      <div class="profile-photo-wrap">
        <img class="profile-photo" src="{avatar}" alt="{html.escape(name)}">
      </div>
    </div>
  </section>

  <main class="container content">
    <div class="grid">
      <div class="card"><h3>About me</h3><p>Background, research interests, and profile information.</p><a href="/about.html">Open page</a></div>
      <div class="card"><h3>Publications</h3><p>Selected manuscripts.</p><a href="/publications.html">Browse publications</a></div>
      <div class="card"><h3>Talks and presentations</h3><p>Talks, presentations, and conference appearances.</p><a href="/talks.html">View talks</a></div>
      <div class="card"><h3>{MAP_LABEL}</h3><p>Explore talks, milestones, and places that have shaped my path.</p><a href="/talkmap/map.html">Open {MAP_LABEL.lower()}</a></div>
      <div class="card"><h3>Posts</h3><p>Writing, commentary, and blog posts.</p><a href="/posts.html">Read posts</a></div>
      <div class="card"><h3>CV</h3><p>Curriculum vitae.</p><a href="/cv.html">View CV</a></div>
    </div>
  </main>

  <footer class="container footer"><p>&copy; 2026 {html.escape(name)}</p></footer>
'''
    return page_shell(site_title, content, site_title)


def render_about(site_title, author, about_html, avatar):
    name = author.get("name", "")
    bio = author.get("bio", "")
    location = author.get("location", "")
    github = author.get("github", "")
    linkedin = author.get("linkedin", "")
    twitter = author.get("twitter", "")
    googlescholar = author.get("googlescholar", "")
    social = []
    if github:
        social.append(f'<a class="social-icon" href="https://github.com/{html.escape(github)}" aria-label="GitHub" title="GitHub">{ICON_GITHUB}</a>')
    if linkedin:
        social.append(f'<a class="social-icon" href="https://www.linkedin.com/in/{html.escape(linkedin)}" aria-label="LinkedIn" title="LinkedIn">{ICON_LINKEDIN}</a>')
    if twitter:
        social.append(f'<a class="social-icon" href="https://x.com/{html.escape(twitter)}" aria-label="X (Twitter)" title="X (Twitter)">{ICON_X}</a>')
    if googlescholar:
        social.append(f'<a class="social-icon" href="{html.escape(googlescholar)}" aria-label="Google Scholar" title="Google Scholar">{ICON_SCHOLAR}</a>')
    social_html = '<div class="social-icons">' + "".join(social) + '</div>' if social else ""
    content = f'''
  <main class="container content page">
    <div class="profile-header">
      <img class="profile-photo small" src="{avatar}" alt="{html.escape(name)}">
      <div>
        <h1>{html.escape(name)}</h1>
        <p class="lead">{html.escape(bio)}</p>
        <p><strong>Location:</strong> {html.escape(location)}</p>
        {social_html}
      </div>
    </div>
    <section class="richtext">{about_html}</section>
  </main>
'''
    return page_shell("About me", content, site_title)


def render_collection_page(site_title, title, intro, items, item_renderer):
    items_html = "\n".join(item_renderer(item) for item in items)
    content = f'''
  <main class="container content page">
    <h1>{html.escape(title)}</h1>
    <p>{html.escape(intro)}</p>
    <div class="listing">{items_html}</div>
  </main>
'''
    return page_shell(title, content, site_title)


def post_card(item):
    tags = item.get("tags") or []
    tags_html = " ".join(f'<span class="tag">{html.escape(str(tag))}</span>' for tag in tags)
    body = item.get("body_html", "")
    return f'''
<article class="card list-card">
  <h3>{html.escape(item.get("title", ""))}</h3>
  <p class="meta">{html.escape(item.get("date", ""))}</p>
  <div>{body}</div>
  <p>{tags_html}</p>
</article>'''


def publication_card(item):
    link = item.get("paperurl", "")
    link_html = f'<p><a href="{html.escape(link)}">Read paper</a></p>' if link else ""
    excerpt = html.escape(item.get("excerpt", ""))
    return f'''
<article class="card list-card">
  <h3>{html.escape(item.get("title", ""))}</h3>
  <p class="meta">{html.escape(item.get("date", ""))} · {html.escape(item.get("venue", ""))}</p>
  <p>{excerpt}</p>
  {link_html}
</article>'''


def talk_card(item):
    body = item.get("body_html", "")
    return f'''
<article class="card list-card">
  <h3>{html.escape(item.get("title", ""))}</h3>
  <p class="meta">{html.escape(item.get("date", ""))} · {html.escape(item.get("venue", ""))}</p>
  <p><strong>Location:</strong> {html.escape(item.get("location", ""))}</p>
  <div>{body}</div>
</article>'''


def fetch_scholar_metrics(scholar_url: str):
    default = {
        "citations": "N/A",
        "h_index": "N/A",
        "i10_index": "N/A",
        "pub_count": "N/A",
    }
    if not scholar_url:
        return default

    try:
        url_with_pagesize = scholar_url if "pagesize" in scholar_url else scholar_url + "&pagesize=100"
        response = requests.get(
            url_with_pagesize,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
    except Exception:
        return default

    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", response.text, flags=re.S | re.I)
    values = {}
    for row in rows:
        m_name = re.search(r'<td[^>]*class="gsc_rsb_sc1"[^>]*>(.*?)</td>', row, flags=re.S | re.I)
        m_value = re.search(r'<td[^>]*class="gsc_rsb_std"[^>]*>(.*?)</td>', row, flags=re.S | re.I)
        if not (m_name and m_value):
            continue
        name = re.sub(r"<.*?>", "", m_name.group(1)).strip().lower()
        value = re.sub(r"<.*?>", "", m_value.group(1)).strip()
        value = html.unescape(value)
        values[name] = value

    pub_rows = re.findall(r'<tr[^>]*class="[^"]*gsc_a_tr[^"]*"[^>]*>', response.text, flags=re.I)
    pub_count = str(len(pub_rows)) if pub_rows else default["citations"]

    return {
        "citations": values.get("citations", default["citations"]),
        "h_index": values.get("h-index", default["h_index"]),
        "i10_index": values.get("i10-index", default["i10_index"]),
        "pub_count": pub_count,
    }


def cv_section_list(items, tab_path, tab_label):
    if not items:
        return ""
    rows = []
    for item in items:
        title = html.escape(item.get("title", "Untitled"))
        rows.append(
            f'<li>{title} — <a href="{tab_path}">See in {tab_label} tab</a></li>'
        )
    return "<ul>" + "".join(rows) + "</ul>"


def cv_page(site_title, author, cv_html, publications, talks):
    name = author.get("name", "")
    bio = author.get("bio", "")
    location = author.get("location", "")
    scholar_url = author.get("googlescholar", "")
    scholar = fetch_scholar_metrics(scholar_url)

    publications_html = cv_section_list(publications, "/publications.html", "Publications")
    talks_html = cv_section_list(talks, "/talks.html", "Talks")
    cv_html = cv_html.replace(
        "<p>See the Publications page for a current list of selected publications.</p>",
        publications_html,
    )
    cv_html = cv_html.replace(
        "<p>See the Talks page for a current list of conference presentations and invited talks.</p>",
        talks_html,
    )

    content = f'''
  <main class="container content page">
    <h1>Curriculum Vitae</h1>
    <section class="metric-grid">
      <article class="metric-card">
        <h3>Publications</h3>
        <p class="metric-value">{html.escape(str(scholar.get("pub_count", len(publications))))}</p>
      </article>
      <article class="metric-card">
        <h3>Citations</h3>
        <p class="metric-value">{html.escape(str(scholar.get("citations", "N/A")))}</p>
      </article>
      <article class="metric-card">
        <h3>h-index</h3>
        <p class="metric-value">{html.escape(str(scholar.get("h_index", "N/A")))}</p>
      </article>
      <article class="metric-card">
        <h3>i10-index</h3>
        <p class="metric-value">{html.escape(str(scholar.get("i10_index", "N/A")))}</p>
      </article>
    </section>
    <p><strong>{html.escape(name)}</strong></p>
    <p>{html.escape(bio)}</p>
    <p><strong>Location:</strong> {html.escape(location)}</p>
    <section class="richtext">{cv_html}</section>
  </main>
'''
    return page_shell("CV", content, site_title)


def load_collection(folder: Path):
    items = []
    for path in sorted(folder.glob("*.md"), reverse=True):
        fm, body = parse_frontmatter(path)
        fm = dict(fm)
        fm["date"] = as_date_str(fm.get("date"))
        fm["body_html"] = md_to_html(body.strip()) if body.strip() else ""
        items.append(fm)
    return items


def main():
    DOCS.mkdir(exist_ok=True)
    # Copy stylesheet so it's always present after a build
    if CSS_SRC.exists():
        (DOCS / "site.css").write_bytes(CSS_SRC.read_bytes())
    # Copy talkmap HTML into docs so the navbar link works
    talkmap_src = ROOT / "talkmap" / "map.html"
    talkmap_dst_dir = DOCS / "talkmap"
    talkmap_dst_dir.mkdir(exist_ok=True)
    if talkmap_src.exists():
        (talkmap_dst_dir / "map.html").write_bytes(talkmap_src.read_bytes())
    config = load_site_config(CONFIG)
    author = config.get("author", {}) or {}
    site_title = config.get("title") or author.get("name") or "Site"
    avatar = resolve_avatar_path()

    about_src = first_existing(ABOUT_QMD, ABOUT_MD)
    _, about_body = parse_frontmatter(about_src) if about_src else ({}, "")
    about_body = remove_about_map_section(strip_liquid(about_body))
    about_html = md_to_html(about_body)

    cv_src = first_existing(CV_QMD)
    _, cv_body = parse_frontmatter(cv_src) if cv_src else ({}, "")
    cv_body = strip_liquid(cv_body)
    cv_html = md_to_html(cv_body)

    posts = load_collection(POSTS)
    publications = load_collection(PUBLICATIONS)
    talks = load_collection(TALKS)

    (DOCS / "index.html").write_text(render_home(site_title, author, avatar), encoding="utf-8")
    (DOCS / "about.html").write_text(render_about(site_title, author, about_html, avatar), encoding="utf-8")
    (DOCS / "posts.html").write_text(render_collection_page(site_title, "Posts", "Writing, commentary, and updates.", posts, post_card), encoding="utf-8")
    (DOCS / "publications.html").write_text(render_collection_page(site_title, "Publications", "Selected publications and research outputs.", publications, publication_card), encoding="utf-8")
    (DOCS / "talks.html").write_text(render_collection_page(site_title, "Talks & Presentations", "Talks, conference appearances, and invited presentations.", talks, talk_card), encoding="utf-8")
    (DOCS / "cv.html").write_text(cv_page(site_title, author, cv_html, publications, talks), encoding="utf-8")


if __name__ == "__main__":
    main()
