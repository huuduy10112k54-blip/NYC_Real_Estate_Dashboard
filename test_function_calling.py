import google.generativeai as genai
import pandas as pd
import os

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
df = pd.DataFrame({'neighborhood': ['Chelsea', 'Brooklyn'], 'sale_price': [1000, 2000]})

def query_dataframe(python_expression: str) -> str:
    '''Runs a python pandas expression on the dataframe 'df' and returns the string result.
    Example expression: df['sale_price'].mean()
    '''
    try:
        print(f"Executing: {python_expression}")
        return str(eval(python_expression, {"df": df, "pd": pd}))
    except Exception as e:
        return f"Error: {e}"

model = genai.GenerativeModel('gemini-1.5-flash', tools=[query_dataframe])
chat = model.start_chat()
resp = chat.send_message("What is the average sale price?")
print("AI Response:", resp.text)