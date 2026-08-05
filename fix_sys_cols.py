import io
import re

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace system_instruction part to include columns
old_sys = '''   - Bạn CÓ THỂ viết code Python pandas để truy vấn bản copy của dữ liệu (biến df_ai).
   - HÃY ĐẶT ĐOẠN CODE ĐÓ VÀO GIỮA THẺ <python> và </python>.'''

new_sys = '''   - Bạn CÓ THỂ viết code Python pandas để truy vấn bản copy của dữ liệu gốc (biến df_ai).
   - Các cột của df_ai bao gồm: {", ".join(df.columns.tolist())}
   - HÃY ĐẶT ĐOẠN CODE ĐÓ VÀO GIỮA THẺ <python> và </python>.'''

text = text.replace(old_sys, new_sys)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)