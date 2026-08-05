import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace SmartDataframe with Agent
text = text.replace('from pandasai import SmartDataframe', 'from pandasai import Agent')
text = text.replace('sdf = SmartDataframe(df_merged, config={"llm": llm})', 'agent = Agent(df_merged, config={"llm": llm, "enable_cache": False})')
text = text.replace('response = sdf.chat(prompt)', 'response = agent.chat(prompt)')

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)