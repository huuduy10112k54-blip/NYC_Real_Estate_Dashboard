import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_code = '''            if 'neigh_stats' in locals() and neigh_stats is not None and len(neigh_stats) > 0:
                # Gộp thông tin lướt sóng (neigh_stats) và dài hạn (long_term) nếu có
                try:
                    import pandas as pd
                    if 'long_term' in locals() and long_term is not None:
                        combined = pd.merge(long_term, neigh_stats[['neighborhood', 'avg_roi', 'avg_profit']], on='neighborhood', how='left')
                    else:
                        combined = neigh_stats'''

new_code = '''            if 'neigh_stats' in locals() and neigh_stats is not None and len(neigh_stats) > 0:
                # long_term đã chứa đầy đủ thông tin gộp của neigh_stats
                try:
                    import pandas as pd
                    if 'long_term' in locals() and long_term is not None:
                        combined = long_term.copy()
                    else:
                        combined = neigh_stats.copy()'''

text = text.replace(old_code, new_code)
with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)