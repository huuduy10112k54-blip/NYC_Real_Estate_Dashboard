import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("flip_rate = row.get('flip_rate', 0) * 100", "flip_rate = row.get('flip_rate', 0)")

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)