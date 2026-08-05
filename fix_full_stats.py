import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_stats = '''            # Tính toán Top thông số
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

new_stats = '''            # Trích xuất toàn bộ dữ liệu thống kê khu vực để AI có thể trả lời chi tiết
            full_stats_str = ""
            if 'neigh_stats' in locals() and neigh_stats is not None and len(neigh_stats) > 0:
                # Gộp thông tin lướt sóng (neigh_stats) và dài hạn (long_term) nếu có
                try:
                    import pandas as pd
                    if 'long_term' in locals() and long_term is not None:
                        combined = pd.merge(long_term, neigh_stats[['neighborhood', 'avg_roi', 'avg_profit']], on='neighborhood', how='left')
                    else:
                        combined = neigh_stats
                    
                    combined = combined.fillna(0).sort_values('total_sales', ascending=False)
                    # Tạo bảng Markdown cho tất cả các khu vực
                    full_stats_str = "| Khu vực | Số giao dịch | Tỷ lệ lướt sóng | ROI (%) | Lợi nhuận ($) |\\n|---|---|---|---|---|\\n"
                    for _, row in combined.iterrows():
                        roi_pct = row.get('avg_roi', 0) * 100
                        flip_rate = row.get('flip_rate', 0) * 100
                        profit = row.get('avg_profit', 0)
                        sales = row.get('total_sales', 0)
                        full_stats_str += f"| {row['neighborhood']} | {sales:,.0f} | {flip_rate:.1f}% | {roi_pct:.1f}% |  |\\n"
                except Exception as e:
                    full_stats_str = f"(Lỗi khi tạo bảng dữ liệu: {e})"
            else:
                full_stats_str = "(Không có đủ dữ liệu để tính toán chi tiết)"
            
            system_instruction = f"""
Bạn là chuyên gia phân tích Dữ liệu Bất Động Sản New York (Data Analyst).
Người dùng đang xem Dashboard phân tích BĐS.

Tổng quan dữ liệu hiện tại:
- Tổng số giao dịch: {total_sales:,}
- Trung bình giá bán: 

BẢNG DỮ LIỆU CHI TIẾT TỪNG KHU VỰC:
(Hãy sử dụng bảng dữ liệu THỰC TẾ này để trả lời bất kỳ câu hỏi nào của người dùng về một khu vực cụ thể, tìm kiếm ROI cao nhất, hoặc so sánh các khu vực)
{full_stats_str}

Nhiệm vụ của bạn:
1. Dựa vào bảng dữ liệu trên để trả lời các câu hỏi về ROI, số giao dịch, khu vực tiềm năng.
2. Nếu người dùng hỏi về một khu vực có trong bảng, hãy trích xuất đúng số liệu.
3. Không bịa đặt số liệu. Nếu dữ liệu không có, hãy nói rõ.
"""'''

text = text.replace(old_stats, new_stats)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)