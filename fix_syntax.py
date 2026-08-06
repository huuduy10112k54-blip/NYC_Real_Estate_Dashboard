import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '''            for m in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
                if m in available_models:
                    model_name = m
                    break
            elif available_models:
                model_name = available_models[0]'''

new_block = '''            for m in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
                if m in available_models:
                    model_name = m
                    break
            else:
                if available_models:
                    model_name = available_models[0]'''

if old_block in text:
    text = text.replace(old_block, new_block)
    with io.open('app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed syntax error")
else:
    print("Could not find the block to replace")