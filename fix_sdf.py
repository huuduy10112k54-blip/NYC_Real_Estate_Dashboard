import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('sdf = SmartDataframe(df, config={', 'agent = Agent(df, config={')

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)