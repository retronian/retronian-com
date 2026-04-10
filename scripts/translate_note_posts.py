#!/usr/bin/env python3
"""Fetch new Japanese articles from note.com/retronian and publish English
translations as Jekyll posts under _posts/.

Detects new articles by comparing the RSS feed against ``note_key`` values in
existing post front matter. For each new article, fetches the full body via
note.com's public note API, asks Claude to translate it faithfully, and writes
a Jekyll-compatible markdown file.

Environment variables:
    ANTHROPIC_API_KEY  Required. Used for translation.
    DRY_RUN            Optional. If set to "1", skip writing files.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "_posts"
RSS_URL = "https://note.com/retronian/rss"
NOTE_API = "https://note.com/api/v3/notes/{key}"
MODEL = "claude-sonnet-4-6"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
NOTE_KEY_RE = re.compile(r"^note_key:\s*(\S+)\s*$", re.MULTILINE)


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "retronian-translator/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def existing_note_keys() -> set[str]:
    keys: set[str] = set()
    for path in POSTS_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        m = FRONT_MATTER_RE.match(text)
        if not m:
            continue
        km = NOTE_KEY_RE.search(m.group(1))
        if km:
            keys.add(km.group(1))
    return keys


def parse_rss() -> list[dict]:
    data = http_get(RSS_URL)
    root = ET.fromstring(data)
    items = []
    for item in root.findall(".//item"):
        link = item.findtext("link") or ""
        key = link.rsplit("/", 1)[-1]
        if not key:
            continue
        pub = item.findtext("pubDate") or ""
        try:
            date = parsedate_to_datetime(pub)
        except (TypeError, ValueError):
            date = datetime.now(timezone.utc)
        items.append(
            {
                "key": key,
                "link": link,
                "title": item.findtext("title") or "",
                "date": date,
            }
        )
    return items


def fetch_note_body(key: str) -> dict:
    raw = http_get(NOTE_API.format(key=key))
    payload = json.loads(raw)
    return payload.get("data", payload)


def translate(title_ja: str, body_html: str, source_url: str) -> dict:
    client = anthropic.Anthropic()
    system = (
        "You are a professional Japanese-to-English translator for a personal "
        "tech blog about retro handheld game consoles. Your job is to translate "
        "faithfully — do not add, remove, invent, or embellish any content. "
        "Preserve the author's casual voice, asides, jokes, and parenthetical "
        "remarks exactly. Preserve all lists, code blocks, links, and structure. "
        "Do not add introductions or conclusions that are not in the source. "
        "The author is the Retronian persona; translate first-person asides "
        "naturally. Output must be valid JSON only."
    )
    user = f"""Translate the following Japanese blog post into English.

Source URL: {source_url}
Original title: {title_ja}

Original body (HTML from note.com):
<<<BODY
{body_html}
BODY

Return a single JSON object with this exact shape:
{{
  "title": "English title (concise, match the Japanese meaning)",
  "slug": "url-friendly-english-slug-lowercase-hyphens",
  "description": "Short meta description (one sentence, <=160 chars)",
  "tags": ["lowercase", "tags", "derived", "from", "content"],
  "body": "Jekyll-compatible Markdown translation of the body. Convert HTML to Markdown. Preserve every sentence, list item, link, and code block from the source. Do not add content not present in the source."
}}

Return ONLY the JSON object, no prose, no code fences."""
    msg = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(block.text for block in msg.content if block.type == "text").strip()
    # Strip accidental code fences if the model adds them.
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n", "", text)
        text = re.sub(r"\n```$", "", text)
    return json.loads(text)


def yaml_string(value: str) -> str:
    """Quote a string safely for YAML front matter."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_post(note: dict, rss_item: dict, translation: dict) -> tuple[Path, str]:
    date = rss_item["date"].astimezone(timezone.utc)
    date_str = date.strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9-]+", "-", translation["slug"].lower()).strip("-") or rss_item["key"]
    filename = f"{date_str}-{slug}.md"
    tags = translation.get("tags") or []
    tag_line = "[" + ", ".join(tags) + "]"
    front_matter = (
        "---\n"
        "layout: post\n"
        f"title: {yaml_string(translation['title'])}\n"
        f"date: {date_str}\n"
        f"description: {yaml_string(translation['description'])}\n"
        f"tags: {tag_line}\n"
        f"note_key: {rss_item['key']}\n"
        f"source_url: {rss_item['link']}\n"
        "---\n\n"
    )
    body = translation["body"].rstrip() + "\n"
    return POSTS_DIR / filename, front_matter + body


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set", file=sys.stderr)
        return 1
    dry_run = os.environ.get("DRY_RUN") == "1"

    existing = existing_note_keys()
    print(f"Known note_keys: {len(existing)}")

    items = parse_rss()
    print(f"RSS items: {len(items)}")

    new_items = [item for item in items if item["key"] not in existing]
    print(f"New items: {len(new_items)}")
    if not new_items:
        return 0

    created: list[str] = []
    for item in new_items:
        print(f"Translating: {item['title']} ({item['key']})")
        note = fetch_note_body(item["key"])
        body_html = note.get("body", "")
        if not body_html:
            print(f"  skip: empty body for {item['key']}")
            continue
        translation = translate(item["title"], body_html, item["link"])
        path, contents = build_post(note, item, translation)
        if path.exists():
            print(f"  skip: {path.name} already exists")
            continue
        if dry_run:
            print(f"  dry-run: would write {path.name}")
            print(contents[:400])
        else:
            path.write_text(contents, encoding="utf-8")
            print(f"  wrote {path.name}")
            created.append(path.name)

    if created and not dry_run:
        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a", encoding="utf-8") as fh:
                fh.write(f"created={','.join(created)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
