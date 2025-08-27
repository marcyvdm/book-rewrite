#!/usr/bin/env python3
"""Count words in text input"""
import sys

if len(sys.argv) > 1:
    # From file
    with open(sys.argv[1]) as f:
        text = f.read()
else:
    # From stdin
    text = sys.stdin.read()

print(len(text.split()))