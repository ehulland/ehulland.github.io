#!/usr/bin/env python3
import os
import re
import yaml
import json
import time
import datetime
import requests

ROOT = os.path.dirname(os.path.dirname(__file__))
TALKS_DIR = os.path.join(ROOT, '_talks')
CACHED_FILE = os.path.join(ROOT, 'talkmap', 'geocache.json')
OUT_DIR = os.path.join(ROOT, 'docs', 'talkmap')
OUT_FILE = os.path.join(OUT_DIR, 'talks.json')

def load_cache():
    if os.path.exists(CACHED_FILE):
        with open(CACHED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHED_FILE), exist_ok=True)
    with open(CACHED_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def parse_frontmatter(path):
    text = open(path, 'r', encoding='utf-8').read()
    m = re.search(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}

def geocode(query, session, cache):
    if not query:
        return None
    if query in cache:
        return cache[query]
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': query, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'ehulland.github.io geocoder'}
    resp = session.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        cache[query] = {'lat': lat, 'lon': lon}
    else:
        cache[query] = None
    # be polite
    time.sleep(1)
    return cache[query]

def clean_location(loc):
    if not loc:
        return loc
    s = str(loc)
    # remove parenthetical virtual notes, standalone 'virtual', and connectors
    s = re.sub(r"\(.*?virtual.*?\)", "", s, flags=re.I)
    s = re.sub(r"\bvirtual\b", "", s, flags=re.I)
    s = re.sub(r"\band\b|\b&\b", ",", s, flags=re.I)
    s = re.sub(r"\s+,\s+", ", ", s)
    s = re.sub(r"\s{2,}", " ", s)
    s = s.strip(' ,')
    return s

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cache = load_cache()
    session = requests.Session()
    talks = []
    for fname in sorted(os.listdir(TALKS_DIR)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(TALKS_DIR, fname)
        fm = parse_frontmatter(path)
        title = fm.get('title') or fname
        date = fm.get('date')
        location = fm.get('location')
        venue = fm.get('venue')
        permalink = fm.get('permalink')
        # clean location strings (remove 'virtual' markers) before geocoding
        loc_query = clean_location(location)
        geoc = geocode(loc_query, session, cache)
        if geoc is None:
            print(f"Warning: no geocode for '{location}' in {fname}")
            continue
        # ensure date is JSON serializable
        if isinstance(date, (datetime.date, datetime.datetime)):
            date_val = date.isoformat()
        else:
            date_val = str(date) if date is not None else None

        talks.append({
            'title': title,
            'date': date_val,
            'location': location,
            'venue': venue,
            'permalink': permalink,
            'lat': geoc['lat'],
            'lon': geoc['lon']
        })
    # sanitize talks values to ensure JSON serializability
    def sanitize(value):
        if isinstance(value, (datetime.date, datetime.datetime)):
            return value.isoformat()
        if isinstance(value, dict):
            return {k: sanitize(v) for k, v in value.items()}
        if isinstance(value, list):
            return [sanitize(v) for v in value]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)

    talks_sanitized = [sanitize(t) for t in talks]
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(talks_sanitized, f, ensure_ascii=False, indent=2)
    save_cache(cache)
    print(f'Wrote {OUT_FILE} with {len(talks)} talks')

if __name__ == '__main__':
    main()
