#!/usr/bin/env python3
"""Get basic book info"""
import json
import sys

with open(sys.argv[1]) as f:
    data = json.load(f)

print("=== BOOK INFO ===")
if 'extraction_metadata' in data:
    print(f"Total pages: {data['extraction_metadata'].get('total_pages', '?')}")
if 'book_metadata' in data:
    print(f"Pages processed: {data['book_metadata'].get('pages_processed', '?')}")
if 'pages' in data:
    print(f"Page data available: {len(data['pages'])} pages")
if 'chapters' in data:
    print(f"Chapters found: {len(data['chapters'])}")
else:
    print("Data structure:", list(data.keys()))