#!/usr/bin/env python3
"""Get text from page range"""
import json
import sys

book_file, start, end = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

with open(book_file) as f:
    data = json.load(f)

pages = data.get('pages', {})
for page_num in range(start, end + 1):
    page_key = str(page_num)
    if page_key in pages:
        page = pages[page_key]
        text = ""
        
        if 'text_blocks' in page:
            for block in page['text_blocks']:
                if 'text' in block:
                    text += block['text'] + "\n"
        elif 'text' in page:
            text += page['text']
        
        print(f"=== PAGE {page_num} ===")
        print(text.strip())
        print()