import io
import re

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r"with tab5:\s*st\.markdown\(\"\"\"\s*<div"
replacement = '''with tab5:
    st.markdown("""
        <div'''

text = re.sub(pattern, replacement, text)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixed indent.")