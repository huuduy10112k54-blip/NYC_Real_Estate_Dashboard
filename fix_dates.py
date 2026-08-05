import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    for prop, group in df_flipped.groupby('property_id'):
        group = group.sort_values('sale_date')
        prices = group['sale_price'].tolist()
        dates = group['sale_date'].tolist()'''

replacement = '''    for prop, group in df_flipped.groupby('property_id'):
        group = group.sort_values('sale_date_parsed')
        prices = group['sale_price'].tolist()
        dates = group['sale_date_parsed'].tolist()'''

if target in text:
    text = text.replace(target, replacement)
    with io.open('app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed successfully')
else:
    print('Target not found')