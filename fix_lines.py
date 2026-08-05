import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    " L?t sng & ?u c (House Flipping)": "🌊 Lướt sóng & Đầu cơ (House Flipping)",
    "Phn tch hnh vi mua i bn l?i (gi? d?i 3 nm) ? t?m ra cc i?m nng ?u c v khu v?c an c l? t?ng.": "Phân tích hành vi mua đi bán lại (giữ dưới 3 năm) để tìm ra các điểm nóng đầu cơ và khu vực an cư lý tưởng.",
    "Khng t?m th?y ? d? li?u giao d?ch l?t sng trong b? l?c hi?n t?i.": "Không tìm thấy đủ dữ liệu giao dịch lướt sóng trong bộ lọc hiện tại.",
    "### ?? Top Khu v?c L?t sng Kh?c li?t nh?t": "### 📈 Top Khu vực Lướt sóng Khốc liệt nhất",
    "Nh ?u t giao d?ch mua i bn l?i lin t?c, thanh kho?n c?c cao nhng r?i ro 'u ?nh' l?n.": "Nhà đầu tư giao dịch mua đi bán lại liên tục, thanh khoản cực cao nhưng rủi ro đu đỉnh lớn.",
    "'S? l?t l?t sng'": "'Số lượt lướt sóng'",
    "'Lợi nhuận TB ($)'": "'Lợi nhuận TB ($)'",
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
    "ang phn tch l?ch s? giao d?ch BBL...": "Đang phân tích lịch sử giao dịch BBL..."
}

# The strings above have standard '?' characters, but we need to replace with \ufffd where it matches the file.
# Wait, actually let me just write a regex that matches the exact structure.
# Or better, let's use the line index since we know exactly where they are!

lines = text.split('\n')

# We can replace by line numbers.
lines[1606] = "            <h2 style='margin:0;font-size:24px;font-weight:700;letter-spacing:-0.5px;'>🌊 Lướt sóng & Đầu cơ (House Flipping)</h2>"
lines[1607] = "            <p style='margin:8px 0 0;font-size:15px;opacity:0.9;'>Phân tích hành vi mua đi bán lại (giữ dưới 3 năm) để tìm ra các điểm nóng đầu cơ và khu vực an cư lý tưởng.</p>"
lines[1611] = "    with st.spinner('Đang phân tích lịch sử giao dịch BBL...'):"
lines[1615] = "        st.warning('Không tìm thấy đủ dữ liệu giao dịch lướt sóng trong bộ lọc hiện tại.')"
lines[1617] = "        st.markdown('### 📈 Top Khu vực Lướt sóng Khốc liệt nhất')"
lines[1618] = "        st.markdown('Nhà đầu tư giao dịch mua đi bán lại liên tục, thanh khoản cực cao nhưng rủi ro đu đỉnh lớn.')"
lines[1623] = "                         labels={'num_flips': 'Số lượt lướt sóng', 'neighborhood': 'Khu vực', 'avg_profit': 'Lợi nhuận TB ($)'},"
lines[1624] = "                         title='Top 5 Khu vực nhiều giao dịch lướt sóng nhất')"
lines[1630] = "        st.markdown('### 💰 Top Khu vực có ROI Lướt sóng cao nhất')"
lines[1631] = "        st.markdown(\"Tỷ suất lợi nhuận (ROI) khổng lồ, phù hợp cho dân đầu cơ 'đánh nhanh rút gọn'.\")"
lines[1638] = "                         title='Top 5 Khu vực có Tỷ suất sinh lời (ROI) lướt sóng cao nhất')"
lines[1644] = "        st.markdown('### 🛡️ Top Khu vực Ổn định (An Cư)')"
lines[1645] = "        st.markdown('Nơi có hàng trăm giao dịch nhưng tỷ lệ lướt sóng rất thấp. Thị trường ổn định, chống lạm phát tốt, lý tưởng để mua ở.')"
lines[1649] = "                              labels={'total_sales': 'Tổng số giao dịch', 'flip_rate': 'Tỷ lệ lướt sóng (%)', 'neighborhood': 'Khu vực'},"
lines[1650] = "                              title='Top 5 Khu vực Ổn định nhất (Tỷ lệ lướt sóng thấp)')"
lines[1660] = "    st.header('💬 Trợ lý AI Phân tích Dữ liệu')"

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Fixed by line numbers!")