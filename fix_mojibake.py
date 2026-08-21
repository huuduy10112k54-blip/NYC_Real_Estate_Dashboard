# -*- coding: utf-8 -*-
"""
Smart Mojibake Fixer for Vietnamese Text.
"""

import os

APP_PATH = 'D:/code/DATN_DP02_NYC/app.py'

vietnamese_chars = 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'
vietnamese_chars += vietnamese_chars.upper()

mapping = {}

# Build CP1252 and CP1258 mappings
for cp in ['cp1252', 'cp1258']:
    for c in vietnamese_chars:
        utf8_bytes = c.encode('utf-8')
        moji = ''
        for b in utf8_bytes:
            try:
                moji += bytes([b]).decode(cp)
            except:
                moji += chr(b)
        if moji != c:
            mapping[moji] = c

# Sort by length descending to replace multi-byte sequences first
sorted_mapping = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)

with open(APP_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

original_text = text

# We must be careful! What if some mojibake overlap?
# Replacing longer strings first handles that.
for moji, correct in sorted_mapping:
    text = text.replace(moji, correct)

# Special fixes if any
text = text.replace('Ä\x90', 'Đ')
text = text.replace('Ä‘', 'đ')

# Write back
with open(APP_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print(f"Fixed! Changed {len(original_text)} to {len(text)} bytes.")
