#!/usr/bin/env python3
import datetime
import html
import re
from pathlib import Path

import markdown
import yaml


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONFIG = ROOT / "_config.yml"
ABOUT_QMD = ROOT / "about.qmd"
ABOUT_MD = ROOT / "_pages" / "about.md"
CV_QMD = ROOT / "cv.qmd"
POSTS = ROOT / "_posts"
PUBLICATIONS = ROOT / "_publications"
TALKS = ROOT / "_talks"
MAP_LABEL = "Journey Map"


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
    ROOT / "headshot-color.jpg",
    ROOT / "headshot_color.jpg",
    ROOT / "images" / "headshot-color.jpg",
    ROOT / "images" / "headshot_color.jpg",
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
    </div>
  </nav>
  {content}
</body>
</html>
'''


def render_home(site_title, author, avatar):
    name = author.get("name", "")
    bio = author.get("bio", "")
    location = author.get("location", "")
    github = author.get("github", "")
    linkedin = author.get("linkedin", "")
    twitter = author.get("twitter", "")
    social = []
    if github:
        social.append(f'<a href="https://github.com/{html.escape(github)}">GitHub</a>')
    if linkedin:
        social.append(f'<a href="https://www.linkedin.com/in/{html.escape(linkedin)}">LinkedIn</a>')
    if twitter:
        social.append(f'<a href="https://x.com/{html.escape(twitter)}">X</a>')
    social_html = " &middot; ".join(social)

    content = f'''
  <section class="hero hero-profile">
    <div class="container hero-grid">
      <div>
        <h1>{html.escape(name)}</h1>
        <p class="lead">{html.escape(bio)}</p>
        <p><strong>Location:</strong> {html.escape(location)}</p>
        <p>{social_html}</p>
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
    content = f'''
  <main class="container content page">
    <div class="profile-header">
      <img class="profile-photo small" src="{avatar}" alt="{html.escape(name)}">
      <div>
        <h1>{html.escape(name)}</h1>
        <p class="lead">{html.escape(bio)}</p>
        <p><strong>Location:</strong> {html.escape(location)}</p>
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


def cv_page(site_title, author, cv_html):
    name = author.get("name", "")
    bio = author.get("bio", "")
    location = author.get("location", "")
    content = f'''
  <main class="container content page">
    <h1>Curriculum Vitae</h1>
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
    (DOCS / "cv.html").write_text(cv_page(site_title, author, cv_html), encoding="utf-8")


if __name__ == "__main__":
    main()
