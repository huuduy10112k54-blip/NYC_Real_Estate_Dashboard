import io
import re

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Pin pandasai version
text = text.replace("pandasai\n", "pandasai<3.0.0\n")

# Replace get_flipping_stats strings
replacements = {
    "Khng t?m th?y ? d? li?u giao d?ch l?t sng trong b? l?c hi?n t?i.": "Không tìm thấy đủ dữ liệu giao dịch lướt sóng trong bộ lọc hiện tại.",
    "### ?? Top Khu v?c L?t sng Kh?c li?t nh?t": "### 📈 Top Khu vực Lướt sóng Khốc liệt nhất",
    "Nh ?u t giao d?ch mua i bn l?i lin t?c, thanh kho?n c?c cao nhng r?i ro 'u ?nh' l?n.": "Nhà đầu tư giao dịch mua đi bán lại liên tục, thanh khoản cực cao nhưng rủi ro đu đỉnh lớn.",
    "S? l?t l?t sng": "Số lượt lướt sóng",
    "Khu v?c": "Khu vực",
    "L?i nhu?n TB ($)": "Lợi nhuận TB ($)",
    "Top 5 Khu v?c nhi?u giao d?ch l?t sng nh?t": "Top 5 Khu vực nhiều giao dịch lướt sóng nhất",
    "T? su?t l?i nhu?n (ROI) kh?ng l?, ph h?p cho dn ?u c 'nh nhanh rt g?n'.": "Tỷ suất lợi nhuận (ROI) khổng lồ, phù hợp cho dân đầu cơ 'đánh nhanh rút gọn'.",
    "Top 5 Khu v?c c T? su?t sinh l?i (ROI) l?t sng cao nh?t": "Top 5 Khu vực có Tỷ suất sinh lời (ROI) lướt sóng cao nhất"
}

for old, new in replacements.items():
    text = text.replace(old, new)

# Also fix requirements.txt
with io.open('requirements.txt', 'r', encoding='utf-8') as f:
    req = f.read()
req = req.replace("pandasai\n", "pandasai<3.0.0\n")
with io.open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(req)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed app.py and requirements.txt")