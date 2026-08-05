import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_model_init = '''            model = genai.GenerativeModel(
                model_name="gemini-pro",
                system_instruction=system_instruction
            )'''

new_model_init = '''            # Tự động tìm model khả dụng tốt nhất
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Ưu tiên các model xịn, nếu không có thì lấy cái đầu tiên
            model_name = "gemini-1.5-flash"
            if "models/gemini-1.5-flash" in available_models:
                model_name = "models/gemini-1.5-flash"
            elif "models/gemini-1.5-pro" in available_models:
                model_name = "models/gemini-1.5-pro"
            elif "models/gemini-pro" in available_models:
                model_name = "models/gemini-pro"
            elif available_models:
                model_name = available_models[0]
                
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )'''

text = text.replace(old_model_init, new_model_init)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)