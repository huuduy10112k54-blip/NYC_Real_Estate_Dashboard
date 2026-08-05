import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.environ.get('GEMINI_API_KEY'))

# Create a sample dataframe
df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6], 'neighborhood': ['Brooklyn', 'Brooklyn', 'Manhattan'], 'sale_price': [1000, 2000, 3000]})

# Create the agent
agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

# Run a query
try:
    response = agent.invoke("What is the average sale price in Brooklyn?")
    print("Response:", response['output'])
except Exception as e:
    print("Error:", e)