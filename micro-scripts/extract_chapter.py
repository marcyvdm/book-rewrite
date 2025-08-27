#!/usr/bin/env python3
"""Extract chapter as JSON"""
import json
import sys
from datetime import datetime

book_file, title, start, end, output_file = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]

with open(book_file) as f:
    data = json.load(f)

pages = data.get('pages', {})
chapter_pages = {}
full_text = ""
paragraphs = []

for page_num in range(start, end + 1):
    page_key = str(page_num)
    if page_key in pages:
        chapter_pages[page_key] = pages[page_key]
        
        # Extract text
        page_text = ""
        if 'text_blocks' in pages[page_key]:
            for block in pages[page_key]['text_blocks']:
                if 'text' in block:
                    page_text += block['text'] + "\n"
        elif 'text' in pages[page_key]:
            page_text += pages[page_key]['text'] + "\n"
        
        full_text += page_text

# Split into paragraphs
para_texts = [p.strip() for p in full_text.split('\n\n') if p.strip()]
paragraphs = [{"content": p, "word_count": len(p.split())} for p in para_texts]

chapter = {
    "title": title,
    "start_page": start,
    "end_page": end,
    "page_count": end - start + 1,
    "word_count": len(full_text.split()),
    "extraction_date": datetime.now().isoformat(),
    "pages": chapter_pages,
    "full_text": full_text.strip(),
    "paragraphs": paragraphs
}

with open(output_file, 'w') as f:
    json.dump(chapter, f, indent=2, ensure_ascii=False)

print(f"Chapter extracted: {len(paragraphs)} paragraphs, {chapter['word_count']} words")