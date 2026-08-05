import io
import re

def fix_file(filepath):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_code = '''        st.markdown("### ?? Top Khu v?c Lý?t sóng Kh?c li?t nh?t")
        st.markdown("Nhà ð?u tý giao d?ch mua ði bán l?i liên t?c, thanh kho?n c?c cao nhýng r?i ro 'ðu ð?nh' l?n.")
        
        top_active = neigh_stats.sort_values('num_flips', ascending=False).head(5)
        fig_act = px.bar(top_active, x='num_flips', y='neighborhood_name', orientation='h',
                         color='avg_profit', color_continuous_scale='RdYlGn',
                         labels={'num_flips': 'S? lý?t lý?t sóng', 'neighborhood_name': 'Khu v?c', 'avg_profit': 'L?i nhu?n TB ($)'},
                         title="Top 5 Khu v?c nhi?u giao d?ch lý?t sóng nh?t")'''
                         
    new_code = '''        st.markdown("### ?? Top Khu v?c Lý?t sóng Kh?c li?t nh?t")
        st.markdown("Tính theo t? l? % s? nhà b? lý?t sóng trên t?ng s? giao d?ch, cho th?y m?t ð? ð?u cõ (Density) th?c s? c?a khu v?c.")
        
        top_active = long_term.sort_values('flip_rate', ascending=False).head(5)
        fig_act = px.bar(top_active, x='flip_rate', y='neighborhood_name', orientation='h',
                         color='avg_profit', color_continuous_scale='RdYlGn',
                         labels={'flip_rate': 'T? l? lý?t sóng (%)', 'neighborhood_name': 'Khu v?c', 'avg_profit': 'L?i nhu?n TB ($)'},
                         title="Top 5 Khu v?c có T? l? Lý?t sóng cao nh?t (%)")'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        with io.open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Replaced successfully in {filepath}')
    else:
        print(f'Old code not found in {filepath}')

fix_file('app.py')
fix_file(r'src\dashboard_postgres.py')
