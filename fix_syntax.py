import io
import re

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace all of system_instruction
# We will use regex to find the start of system_instruction = f""" and end of it.
import re
match = re.search(r'system_instruction = f"""(.*?)"""\s*Nhiệm vụ của bạn:(.*?)"""', text, re.DOTALL)
if match:
    old_full = match.group(0)
    print("Found messy system instruction.")
else:
    # Just grab everything from system_instruction to the next genai.list_models()
    match = re.search(r'(system_instruction = f"""(.*?)""")', text, re.DOTALL)
    print("Found standard system instruction.")

# We will just replace everything between system_instruction = f""" and vailable_models =
match = re.search(r'(system_instruction = f""".*?""".*?)# Tự động tìm model', text, re.DOTALL)
if match:
    old_block = match.group(1)
    new_block = '''system_instruction = f"""
Bạn là chuyên gia phân tích Dữ liệu Bất Động Sản New York (Data Analyst).
Người dùng đang xem Dashboard phân tích BĐS.

Tổng quan dữ liệu hiện tại:
- Tổng số giao dịch: {total_sales:,}
- Trung bình giá bán: 

BẢNG DỮ LIỆU CHI TIẾT TỪNG KHU VỰC:
(Hãy sử dụng bảng dữ liệu THỰC TẾ này để trả lời các câu hỏi phổ biến)
{full_stats_str}

Nhiệm vụ của bạn:
1. Dựa vào bảng dữ liệu trên để trả lời các câu hỏi về ROI, số giao dịch.
2. NẾU người dùng hỏi một câu hỏi ĐẶC BIỆT yêu cầu truy vấn DỮ LIỆU THÔ (Ví dụ: "Căn nhà đắt nhất giá bao nhiêu?", "Có bao nhiêu nhà bán dưới 500 ngàn đô?"):
   - Bạn CÓ THỂ viết code Python pandas để truy vấn bản copy của dữ liệu (biến df_ai).
   - HÃY ĐẶT ĐOẠN CODE ĐÓ VÀO GIỮA THẺ <python> và </python>.
   - Ví dụ: <python>df_ai['sale_price'].max()</python>
   - Chỉ được viết MỘT BIỂU THỨC (expression) duy nhất, KHÔNG gán biến.
   - Hệ thống sẽ chạy đoạn code này và trả về kết quả cho bạn để bạn trả lời người dùng.
3. Nếu không cần tính toán nâng cao, hãy trả lời bình thường.
"""
            
            '''
    text = text.replace(old_block, new_block)
    with io.open('app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully!")
else:
    print("Could not find the block to replace.")