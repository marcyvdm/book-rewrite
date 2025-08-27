#!/usr/bin/env python3
"""Count total pages in book"""
import json
import sys

with open(sys.argv[1]) as f:
    data = json.load(f)

print(len(data.get('pages', {})))