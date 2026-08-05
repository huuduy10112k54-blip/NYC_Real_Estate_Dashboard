import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_chat = '''                            # ReAct Loop: Kiểm tra xem AI có muốn chạy code không
                            if "<python>" in response.text:
                                import re
                                match = re.search(r'<python>(.*?)</python>', response.text, re.DOTALL)
                                if match:
                                    code = match.group(1).strip()
                                    try:
                                        # Tạo bản copy an toàn theo yêu cầu của người dùng
                                        df_ai = df.copy(deep=True)
                                        # Cho phép các thư viện cơ bản
                                        eval_globals = {"__builtins__": {}}
                                        eval_locals = {"df_ai": df_ai, "pd": __import__('pandas')}
                                        
                                        # Thực thi biểu thức
                                        res = eval(code, eval_globals, eval_locals)
                                        
                                        # Gửi kết quả lại cho AI để tạo câu trả lời cuối cùng
                                        follow_up_prompt = f"Kết quả chạy code trên bản copy: {res}\\nHãy trả lời người dùng dựa trên kết quả này."
                                        response = chat.send_message(follow_up_prompt)
                                    except Exception as e:
                                        # Nếu lỗi, báo cho AI biết để xin lỗi hoặc thử lại
                                        response = chat.send_message(f"Hệ thống báo lỗi khi chạy code: {e}\\nHãy xin lỗi người dùng và giải thích lỗi.")
                                        
                            st.markdown(response.text)'''

new_chat = '''                            # ReAct Loop: Cho phép AI truy vấn nhiều lần (tối đa 3 lần)
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
                            final_text = re.sub(r'<python>.*?</python>', '', response.text, flags=re.DOTALL).strip()
                            st.markdown(final_text)
                            response.text = final_text # Update text to save cleanly in history'''

text = text.replace(old_chat, new_chat)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)