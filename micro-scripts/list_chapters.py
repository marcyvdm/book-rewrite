#!/usr/bin/env python3
"""List chapters from structured book"""
import json
import sys

with open(sys.argv[1]) as f:
    data = json.load(f)

chapters = data.get('chapters', [])
print(f"Total chapters: {len(chapters)}")

for i, chapter in enumerate(chapters):
    title = chapter.get('title', 'No title')
    page = chapter.get('page_start', '?')
    print(f"{i+1}. {title} (Page {page})")