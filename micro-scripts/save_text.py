#!/usr/bin/env python3
"""Save stdin to file"""
import sys

with open(sys.argv[1], 'w') as f:
    f.write(sys.stdin.read())