import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start of tab5 and start of tab6
start_tab5 = -1
end_tab6 = -1

for i, line in enumerate(lines):
    if line.startswith('with tab5:'):
        start_tab5 = i
    elif line.strip() == 'st.stop()':
        if start_tab5 != -1 and i > start_tab5:
            # We assume the first st.stop() after tab5 is the one in tab6 error block
            end_tab6 = i
            break

if start_tab5 != -1 and end_tab6 != -1:
    clean_code = '''with tab5:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#4338ca,#6366f1,#818cf8);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(99,102,241,0.35)'>
        <h2 style='margin:0;font-size:24px;font-weight:700;letter-spacing:-0.5px;'>🌊 Lướt sóng & Đầu cơ (House Flipping)</h2>
        <p style='margin:8px 0 0;font-size:15px;opacity:0.9;'>Phân tích hành vi mua đi bán lại (giữ dưới 3 năm) để tìm ra các điểm nóng đầu cơ và khu vực an cư lý tưởng.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Đang phân tích lịch sử giao dịch BBL..."):
        df_flip, neigh_stats, long_term = get_flipping_stats(df)
        
    if neigh_stats is None or len(neigh_stats) == 0:
        st.warning("Không tìm thấy đủ dữ liệu giao dịch lướt sóng trong bộ lọc hiện tại.")
    else:
        st.markdown("### 📈 Top Khu vực Lướt sóng Khốc liệt nhất")
        st.markdown("Nhà đầu tư giao dịch mua đi bán lại liên tục, thanh khoản cực cao nhưng rủi ro đu đỉnh lớn.")
        
        top_active = long_term.sort_values('flip_rate', ascending=False).head(5)
        fig_act = px.bar(top_active, x='flip_rate', y='neighborhood', orientation='h',
                         color='avg_profit', color_continuous_scale='RdYlGn',
                         labels={'num_flips': 'Số lượt lướt sóng', 'neighborhood': 'Khu vực', 'avg_profit': 'Lợi nhuận TB ($)'},
                         title="Top 5 Khu vực nhiều giao dịch lướt sóng nhất")
        fig_act.update_layout(yaxis={'categoryorder':'total ascending'})
        clayout(fig_act, h=350)
        st.plotly_chart(fig_act, width='stretch')
        
        divider()
        st.markdown("### 💰 Top Khu vực có ROI Lướt sóng cao nhất")
        st.markdown("Tỷ suất lợi nhuận (ROI) khổng lồ, phù hợp cho dân đầu cơ 'đánh nhanh rút gọn'.")
        
        top_roi = neigh_stats.sort_values('avg_roi', ascending=False).head(5)
        top_roi['roi_pct'] = top_roi['avg_roi'] * 100
        fig_roi = px.bar(top_roi, x='roi_pct', y='neighborhood', orientation='h',
                         color='roi_pct', color_continuous_scale='Sunsetdark',
                         labels={'roi_pct': 'ROI TB (%)', 'neighborhood': 'Khu vực'},
                         title="Top 5 Khu vực có Tỷ suất sinh lời (ROI) lướt sóng cao nhất")
        fig_roi.update_layout(yaxis={'categoryorder':'total ascending'})
        clayout(fig_roi, h=350)
        st.plotly_chart(fig_roi, width='stretch')
        
        divider()
        st.markdown("### 🛡️ Top Khu vực Ổn định (An Cư)")
        st.markdown("Nơi có hàng trăm giao dịch nhưng tỷ lệ lướt sóng rất thấp. Thị trường ổn định, chống lạm phát tốt, lý tưởng để mua ở.")
        
        top_safe = long_term.sort_values('flip_rate', ascending=True).head(5)
        fig_safe = px.scatter(top_safe, x='total_sales', y='flip_rate', size='total_sales', color='neighborhood',
                              labels={'total_sales': 'Tổng số giao dịch', 'flip_rate': 'Tỷ lệ lướt sóng (%)', 'neighborhood': 'Khu vực'},
                              title="Top 5 Khu vực Ổn định nhất (Tỷ lệ lướt sóng thấp)")
        clayout(fig_safe, h=350)
        st.plotly_chart(fig_safe, width='stretch')



# ============================================================
# TAB 6 – TRỢ LÝ AI (PANDASAI)
# ============================================================
with tab6:
    st.header("💬 Trợ lý AI Phân tích Dữ liệu")
    st.markdown("---")
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.warning("⚠️ Chưa tìm thấy API Key. Vui lòng thêm GEMINI_API_KEY vào file .env")
    else:
        try:
            from pandasai import SmartDataframe
            from pandasai.llm import GoogleGemini
        except Exception as e:
            import traceback
            st.error(f"Lỗi khởi tạo PandasAI: {type(e).__name__} - {str(e)}")
            st.code(traceback.format_exc())
            st.stop()
'''
    new_lines = lines[:start_tab5] + [clean_code + '\n'] + lines[end_tab6+1:]
    with io.open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Replaced chunk successfully!")
else:
    print("Could not find start_tab5 or end_tab6")