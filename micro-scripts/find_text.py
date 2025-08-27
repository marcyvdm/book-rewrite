#!/usr/bin/env python3
"""Find text in book, return page numbers"""
import json
import sys

book_file, search_text = sys.argv[1], sys.argv[2]
fuzzy = "--fuzzy" in sys.argv

with open(book_file) as f:
    data = json.load(f)

search_lower = search_text.lower()
pages = data.get('pages', {})

for page_key in sorted(pages.keys(), key=int):
    page = pages[page_key]
    text = ""
    
    if 'text_blocks' in page:
        for block in page['text_blocks']:
            if 'text' in block:
                text += block['text'] + " "
    elif 'text' in page:
        text += page['text']
    
    if search_lower in text.lower():
        print(f"{page_key}")
        break