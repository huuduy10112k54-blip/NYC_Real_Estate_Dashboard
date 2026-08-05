import io
import re

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Tab 5 header block
pattern = r"with tab5:.*?st\.markdown\(\"\"\"\s*<div[^>]*>.*?</div>\s*\"\"\", unsafe_allow_html=True\)"
replacement = '''with tab5:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#4338ca,#6366f1,#818cf8);border-radius:14px;
        padding:18px 24px;color:#fff;margin-bottom:22px;
        box-shadow:0 6px 24px rgba(99,102,241,0.35)'>
            <h2 style='margin:0;font-size:24px;font-weight:700;letter-spacing:-0.5px;'>🌊 Lướt sóng & Đầu cơ (House Flipping)</h2>
            <p style='margin:8px 0 0;font-size:15px;opacity:0.9;'>Phân tích hành vi mua đi bán lại (giữ dưới 3 năm) để tìm ra các điểm nóng đầu cơ và khu vực an cư lý tưởng.</p>
        </div>
        """, unsafe_allow_html=True)'''

text = re.sub(pattern, replacement, text, flags=re.DOTALL)

# Replace spinner
pattern_spinner = r"with st\.spinner\(\"[^\"]*\"\):"
text = re.sub(pattern_spinner, 'with st.spinner("Đang phân tích lịch sử giao dịch BBL..."):', text)

# Replace warning
pattern_warning = r"st\.warning\(\"[^\"]*\"\)"
text = re.sub(pattern_warning, 'st.warning("Không tìm thấy đủ dữ liệu giao dịch lướt sóng trong bộ lọc hiện tại.")', text)

# Replace markdown top
pattern_top = r"st\.markdown\(\"### \?\? Top Khu v\?c[^\"]*\"\)"
text = re.sub(pattern_top, 'st.markdown("### 📈 Top Khu vực Lướt sóng Khốc liệt nhất")', text)

pattern_desc = r"st\.markdown\(\"Nh[^\\\"]*\"\)"
text = re.sub(pattern_desc, 'st.markdown("Nhà đầu tư giao dịch mua đi bán lại liên tục, thanh khoản cực cao nhưng rủi ro đu đỉnh lớn.")', text)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed encoding.")