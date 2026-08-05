import io
import re

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r"except ImportError:\s*st\.error\(\"Thư viện 'pandasai' chưa được cài đặt[^\"]*\"\)"
replacement = '''except Exception as e:
            import traceback
            st.error(f"Lỗi khởi tạo PandasAI: {type(e).__name__} - {str(e)}")
            st.code(traceback.format_exc())'''

if re.search(pattern, text):
    text = re.sub(pattern, replacement, text)
    with io.open('app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced try-except.")
else:
    print("Pattern not found.")