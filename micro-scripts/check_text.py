#!/usr/bin/env python3
"""Check if text contains expected content"""
import sys

if len(sys.argv) < 3:
    print("Usage: check_text.py <file> <keyword1> [keyword2] ...")
    sys.exit(1)

text_file = sys.argv[1]
keywords = sys.argv[2:]

with open(text_file) as f:
    content = f.read().lower()

found = 0
for keyword in keywords:
    if keyword.lower() in content:
        found += 1

print(f"{found}/{len(keywords)}")