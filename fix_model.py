import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('model_name="gemini-1.5-flash"', 'model_name="gemini-pro"')

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)