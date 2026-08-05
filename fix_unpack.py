import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍  Tổng quan",
    "🏢  Phân tích khu vực",
    "📊  Yếu tố quyết định giá",
    "Xu hướng & Khuyến nghị đầu tư",
    "🤖  Dự báo & Mô hình ML",
    "🌊 Lướt sóng & Đầu cơ",
])'''

replacement = '''tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍  Tổng quan",
    "🏢  Phân tích khu vực",
    "📊  Yếu tố quyết định giá",
    "Xu hướng & Khuyến nghị đầu tư",
    "🤖  Dự báo & Mô hình ML",
    "🌊 Lướt sóng & Đầu cơ",
    "💬 Trợ lý AI (Phân tích Data)",
])'''

if target in text:
    text = text.replace(target, replacement)
    with io.open('app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed successfully')
else:
    print('Target not found')