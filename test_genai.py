import google.generativeai as genai
import pandas as pd
import os

genai.configure(api_key=os.environ.get('GEMINI_API_KEY', ''))
model = genai.GenerativeModel('gemini-1.5-flash')
df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]})
context = f"Data schema: {df.dtypes.to_dict()}\nSample data:\n{df.head().to_markdown()}"
print("Model initialized")