import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_stats = '''            # Tính toán một số thống kê cơ bản từ dataframe để đưa vào ngữ cảnh AI
            avg_price = df['sale_price'].dropna().mean() if 'sale_price' in df.columns else 0
            total_sales = len(df)
            neighborhoods = df['neighborhood'].dropna().unique().tolist() if 'neighborhood' in df.columns else []
            neighborhoods_str = ", ".join(neighborhoods[:20]) + ("..." if len(neighborhoods) > 20 else "")
            
            system_instruction = f"""
Bạn là chuyên gia phân tích Dữ liệu Bất Động Sản New York (Data Analyst).
Người dùng đang xem Dashboard phân tích BĐS với bộ lọc hiện tại.
Dữ liệu hiện tại (đã lọc) có các thông số sau:
- Tổng số giao dịch: {total_sales:,}
- Trung bình giá bán: 
- Các khu vực trong dữ liệu: {neighborhoods_str}'''

new_stats = '''            # Tính toán một số thống kê cơ bản từ dataframe để đưa vào ngữ cảnh AI
            avg_price = df['sale_price'].dropna().mean() if 'sale_price' in df.columns else 0
            total_sales = len(df)
            neighborhoods = df['neighborhood'].dropna().unique().tolist() if 'neighborhood' in df.columns else []
            neighborhoods_str = ", ".join(neighborhoods[:20]) + ("..." if len(neighborhoods) > 20 else "")
            
            # Tính toán Top thông số
            top_sales_str = ""
            top_roi_str = ""
            if 'neigh_stats' in locals() and neigh_stats is not None and len(neigh_stats) > 0:
                top_roi = neigh_stats.sort_values('avg_roi', ascending=False).head(5)
                top_roi_str = "\\n".join([f"- {row['neighborhood']}: Tỷ suất lợi nhuận (ROI) trung bình {row['avg_roi']*100:.1f}%, lợi nhuận TB " for _, row in top_roi.iterrows()])
            else:
                top_roi_str = "(Không có đủ dữ liệu lướt sóng để tính ROI)"
                
            if 'long_term' in locals() and long_term is not None and len(long_term) > 0:
                top_sales = long_term.sort_values('total_sales', ascending=False).head(5)
                top_sales_str = "\\n".join([f"- {row['neighborhood']}: {row['total_sales']} giao dịch" for _, row in top_sales.iterrows()])
            else:
                top_sales_str = "(Không có đủ dữ liệu giao dịch)"
            
            system_instruction = f"""
Bạn là chuyên gia phân tích Dữ liệu Bất Động Sản New York (Data Analyst).
Người dùng đang xem Dashboard phân tích BĐS với bộ lọc hiện tại.
Dữ liệu hiện tại (đã lọc) có các thông số sau:
- Tổng số giao dịch: {total_sales:,}
- Trung bình giá bán: 
- Các khu vực trong dữ liệu: {neighborhoods_str}

Thống kê chi tiết (Dữ liệu thực tế từ hệ thống, hãy dùng dữ liệu này để trả lời!):
Top 5 khu vực giao dịch nhiều nhất:
{top_sales_str}

Top 5 khu vực có tỷ suất lợi nhuận (ROI) lướt sóng cao nhất:
{top_roi_str}'''

text = text.replace(old_stats, new_stats)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)