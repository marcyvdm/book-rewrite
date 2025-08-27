#!/usr/bin/env python3
"""Get text from a single page"""
import json
import sys

book_file, page_num = sys.argv[1], int(sys.argv[2])

with open(book_file) as f:
    data = json.load(f)

page_key = str(page_num)
if page_key not in data.get('pages', {}):
    exit(1)

page = data['pages'][page_key]
text = ""

if 'text_blocks' in page:
    for block in page['text_blocks']:
        if 'text' in block:
            text += block['text'] + "\n"
elif 'text' in page:
    text += page['text']

print(text.strip())