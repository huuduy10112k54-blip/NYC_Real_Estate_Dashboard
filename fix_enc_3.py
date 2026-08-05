import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    "?? L?t sng & ?u c (House Flipping)": "🌊 Lướt sóng & Đầu cơ (House Flipping)",
    "Phn tch hnh vi mua i bn l?i (gi? d?i 3 nm) ? t?m ra cc i?m nng ?u c v khu v?c an c l? t?ng.": "Phân tích hành vi mua đi bán lại (giữ dưới 3 năm) để tìm ra các điểm nóng đầu cơ và khu vực an cư lý tưởng.",
    "Khng t?m th?y ? d? li?u giao d?ch l?t sng trong b? l?c hi?n t?i.": "Không tìm thấy đủ dữ liệu giao dịch lướt sóng trong bộ lọc hiện tại.",
    "### ?? Top Khu v?c L?t sng Kh?c li?t nh?t": "### 📈 Top Khu vực Lướt sóng Khốc liệt nhất",
    "Nh ?u t giao d?ch mua i bn l?i lin t?c, thanh kho?n c?c cao nhng r?i ro 'u ?nh' l?n.": "Nhà đầu tư giao dịch mua đi bán lại liên tục, thanh khoản cực cao nhưng rủi ro đu đỉnh lớn.",
    "'S? l?t l?t sng'": "'Số lượt lướt sóng'",
    "'Khu v?c'": "'Khu vực'",
    "'L?i nhu?n TB ($)'": "'Lợi nhuận TB ($)'",
    "Top 5 Khu v?c nhi?u giao d?ch l?t sng nh?t": "Top 5 Khu vực nhiều giao dịch lướt sóng nhất",
    "### ?? Top Khu v?c L?t sng Siu l?i nhu?n": "### 💰 Top Khu vực có ROI Lướt sóng cao nhất",
    "T? su?t l?i nhu?n (ROI) kh?ng l?, ph h?p cho dn ?u c 'nh nhanh rt g?n'.": "Tỷ suất lợi nhuận (ROI) khổng lồ, phù hợp cho dân đầu cơ 'đánh nhanh rút gọn'.",
    "Top 5 Khu v?c c T? su?t sinh l?i (ROI) l?t sng cao nh?t": "Top 5 Khu vực có Tỷ suất sinh lời (ROI) lướt sóng cao nhất",
    "### ?? Top Khu v?c ?n ?nh (An C)": "### 🛡️ Top Khu vực Ổn định (An Cư)",
    "Ni c hng trm giao d?ch nhng t? l? l?t sng r?t th?p. Th? tr?ng ?n ?nh, ch?ng l?m pht t?t, l? t?ng ? mua ?.": "Nơi có hàng trăm giao dịch nhưng tỷ lệ lướt sóng rất thấp. Thị trường ổn định, chống lạm phát tốt, lý tưởng để mua ở.",
    "'T?ng s? giao d?ch'": "'Tổng số giao dịch'",
    "'T? l? l?t sng (%)'": "'Tỷ lệ lướt sóng (%)'",
    "Top 5 Khu v?c ?n ?nh nh?t (T? l? l?t sng th?p)": "Top 5 Khu vực Ổn định nhất (Tỷ lệ lướt sóng thấp)",
    "?? Tr? l AI Phn tch D? li?u": "💬 Trợ lý AI Phân tích Dữ liệu",
    "Khng c khu v?c no ?t ? i?u ki?n thanh kho?n (>= 30 giao d?ch) trong b? l?c hi?n t?i.": "Không có khu vực nào đạt đủ điều kiện thanh khoản (>= 30 giao dịch) trong bộ lọc hiện tại."
}

for old, new in replacements.items():
    text = text.replace(old, new)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Properly restored.")