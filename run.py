import io
def fix_file(filepath):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("top_active = neigh_stats.sort_values('num_flips', ascending=False).head(5)", "top_active = long_term.sort_values('flip_rate', ascending=False).head(5)")
    content = content.replace("fig_act = px.bar(top_active, x='num_flips', y='neighborhood_name', orientation='h',", "fig_act = px.bar(top_active, x='flip_rate', y='neighborhood_name', orientation='h',")
    with io.open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(b'Done: ' + filepath.encode('utf-8'))

fix_file('app.py')
fix_file(r'src\dashboard_postgres.py')
