import google.generativeai as genai
import pandas as pd
import os
import re

genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'dummy'))

# dummy mock for testing since I don't have api key
def mock_send_message(prompt):
    class Resp:
        pass
    r = Resp()
    if "Căn nhà đắt nhất" in prompt:
        r.text = "<python>df_ai['sale_price'].max()</python>"
    else:
        r.text = f"Căn nhà đắt nhất có giá {prompt.split('Kết quả từ hệ thống: ')[-1].split()[0]}"
    return r

df = pd.DataFrame({'sale_price': [1000, 5000, 2000]})

chat = type('MockChat', (), {'send_message': lambda self, p: mock_send_message(p)})()

prompt = "Căn nhà đắt nhất giá bao nhiêu?"
response = chat.send_message(prompt)
print("Initial:", response.text)

if "<python>" in response.text:
    match = re.search(r'<python>(.*?)</python>', response.text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        print("Extracted code:", code)
        try:
            df_ai = df.copy(deep=True)
            res = eval(code, {"__builtins__": {}}, {"df_ai": df_ai, "pd": pd})
            print("Eval result:", res)
            response = chat.send_message(f"Kết quả từ hệ thống: {res}\nHãy trả lời người dùng dựa trên kết quả này.")
        except Exception as e:
            response = chat.send_message(f"Lỗi: {e}")
            
print("Final response:", response.text)