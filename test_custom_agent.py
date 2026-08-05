import google.generativeai as genai
import pandas as pd
import os
import re

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6], 'neighborhood': ['Brooklyn', 'Brooklyn', 'Manhattan'], 'sale_price': [1000, 2000, 3000]})

question = "What is the average sale price in Brooklyn?"

prompt1 = f'''
You have a pandas dataframe df.
Columns: {list(df.columns)}
Question: {question}

Return ONLY a Python pandas expression that computes the answer. The expression should evaluate to the final answer (a number, string, or small summary). Do NOT wrap it in markdown. Do NOT assign to variables. Just the expression, starting with df.
Example: df['sale_price'].mean()
'''

model = genai.GenerativeModel('gemini-pro')
resp1 = model.generate_content(prompt1).text.strip()
# strip markdown if it accidentally added it
resp1 = re.sub(r'^\\\python', '', resp1)
resp1 = re.sub(r'^\\\', '', resp1)
resp1 = re.sub(r'\\\$', '', resp1)
resp1 = resp1.strip()

print("Generated code:", resp1)

try:
    # Safely evaluate it
    result = eval(resp1, {'df': df, 'pd': pd})
    print("Execution result:", result)
    
    prompt2 = f'''
Question: {question}
Calculated Result: {result}

Answer the question naturally based on the result.
'''
    resp2 = model.generate_content(prompt2).text.strip()
    print("Final answer:", resp2)
except Exception as e:
    print("Error:", e)