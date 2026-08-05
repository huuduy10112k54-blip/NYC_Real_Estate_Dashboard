import io
import re

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# REPLACE SYSTEM PROMPT
old_sys = '''2. NẾU người dùng hỏi một câu hỏi ĐẶC BIỆT yêu cầu truy vấn DỮ LIỆU THÔ (Ví dụ: "Căn nhà đắt nhất giá bao nhiêu?", "Có bao nhiêu nhà bán dưới 500 ngàn đô?"):
   - Bạn CÓ THỂ viết code Python pandas để truy vấn bản copy của dữ liệu gốc (biến df_ai).
   - Các cột của df_ai bao gồm: {", ".join(df.columns.tolist())}
   - HÃY ĐẶT ĐOẠN CODE ĐÓ VÀO GIỮA THẺ <python> và </python>.
   - Ví dụ: <python>df_ai['sale_price'].max()</python>
   - Chỉ được viết MỘT BIỂU THỨC (expression) duy nhất, KHÔNG gán biến.
   - Hệ thống sẽ chạy đoạn code này và trả về kết quả cho bạn để bạn trả lời người dùng.'''

new_sys = '''2. NẾU người dùng hỏi một câu hỏi ĐẶC BIỆT yêu cầu truy vấn DỮ LIỆU THÔ (Ví dụ: "Nhà dưới 300k cho 5 người ở", "Căn nhà đắt nhất giá bao nhiêu?"):
   - Bắt buộc phải dùng truy vấn SQL để tra cứu trên bảng cơ sở dữ liệu ảo tên là df.
   - Các cột của bảng df bao gồm: {", ".join(df.columns.tolist())}
   - Cột is_residential (True/False), cột esidential_units (số lượng phòng/người ở).
   - HÃY ĐẶT CÂU LỆNH SQL VÀO GIỮA THẺ <sql> và </sql>.
   - Ví dụ: <sql>SELECT neighborhood, count(*) FROM df WHERE sale_price <= 300000 AND is_residential = True GROUP BY neighborhood ORDER BY count(*) DESC LIMIT 5</sql>
   - Hệ thống sẽ chạy SQL qua thư viện DuckDB siêu tốc và trả kết quả cho bạn để bạn tư vấn.'''

text = text.replace(old_sys, new_sys)

# REPLACE EXECUTION LOOP
old_exec = '''                            # ReAct Loop: Cho phép AI truy vấn nhiều lần (tối đa 3 lần)
                            for _ in range(3):
                                if "<python>" in response.text:
                                    import re
                                    # Lấy khối code đầu tiên
                                    match = re.search(r'<python>(.*?)</python>', response.text, re.DOTALL)
                                    if match:
                                        code = match.group(1).strip()
                                        try:
                                            df_ai = df.copy(deep=True)
                                            eval_globals = {"__builtins__": {}}
                                            eval_locals = {"df_ai": df_ai, "pd": __import__('pandas')}
                                            
                                            # Trích xuất dữ liệu an toàn
                                            res = eval(code, eval_globals, eval_locals)
                                            
                                            # Yêu cầu AI tiếp tục phân tích hoặc kết luận
                                            follow_up_prompt = f"Kết quả hệ thống trả về: {res}\\nNếu cần truy vấn thêm, hãy viết thẻ <python>. Nếu đã đủ thông tin, hãy tổng hợp và trả lời trực tiếp cho người dùng. TUYỆT ĐỐI không in ra thẻ <python> cho người dùng xem."
                                            response = chat.send_message(follow_up_prompt)
                                        except Exception as e:
                                            response = chat.send_message(f"Lỗi cú pháp Python: {e}\\nHãy sửa lại code và gửi lại thẻ <python> mới.")
                                    else:
                                        break
                                else:
                                    break
                                    
                            # Lọc bỏ bất kỳ thẻ python nào còn sót lại trước khi hiện cho người dùng
                            import re
                            final_text = re.sub(r'<python>.*?</python>', '', response.text, flags=re.DOTALL).strip()'''

new_exec = '''                            # Text-to-SQL (DuckDB): Gọi duy nhất 1 lần để tiết kiệm API
                            if "<sql>" in response.text:
                                import re
                                match = re.search(r'<sql>(.*?)</sql>', response.text, re.DOTALL | re.IGNORECASE)
                                if match:
                                    sql_query = match.group(1).strip()
                                    try:
                                        import duckdb
                                        # DuckDB sẽ tự động nhận diện biến 'df' (pandas DataFrame) đang tồn tại trong global namespace
                                        # Hoặc an toàn hơn, đăng ký trực tiếp DataFrame vào bộ nhớ DuckDB tạm thời
                                        conn = duckdb.connect()
                                        conn.register('df', df)
                                        res_df = conn.execute(sql_query).df()
                                        conn.close()
                                        
                                        # Chuyển Dataframe kết quả thành dạng chữ để đưa cho AI
                                        res_str = res_df.to_string()
                                        if len(res_str) > 2000:
                                            res_str = res_str[:2000] + "\\n... (Dữ liệu đã bị cắt bớt do quá dài)"
                                            
                                        follow_up_prompt = f"Kết quả truy vấn SQL từ DB:\\n{res_str}\\n\\nDựa vào kết quả này, hãy trả lời câu hỏi của người dùng một cách chuyên nghiệp. KHÔNG HIỂN THỊ thẻ <sql> nữa."
                                        response = chat.send_message(follow_up_prompt)
                                    except Exception as e:
                                        response = chat.send_message(f"Lỗi truy vấn SQL: {e}\\nHãy xin lỗi người dùng và thử tự ước lượng dựa trên kiến thức chung.")
                                        
                            # Lọc bỏ bất kỳ thẻ sql nào còn sót lại trước khi hiện cho người dùng
                            import re
                            final_text = re.sub(r'<sql>.*?</sql>', '', response.text, flags=re.DOTALL | re.IGNORECASE).strip()'''

text = text.replace(old_exec, new_exec)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done replacement.")