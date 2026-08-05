import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace system_instruction part
old_sys = '''BẢNG DỮ LIỆU CHI TIẾT TỪNG KHU VỰC:
(Hãy sử dụng bảng dữ liệu THỰC TẾ này để trả lời bất kỳ câu hỏi nào của người dùng về một khu vực cụ thể, tìm kiếm ROI cao nhất, hoặc so sánh các khu vực)
{full_stats_str}

Nhiệm vụ của bạn:
1. Dựa vào bảng dữ liệu trên để trả lời các câu hỏi về ROI, số giao dịch, khu vực tiềm năng.
2. Nếu người dùng hỏi về một khu vực có trong bảng, hãy trích xuất đúng số liệu.
3. Không bịa đặt số liệu. Nếu dữ liệu không có, hãy nói rõ.
"""'''

new_sys = '''BẢNG DỮ LIỆU CHI TIẾT TỪNG KHU VỰC:
(Hãy sử dụng bảng dữ liệu THỰC TẾ này để trả lời các câu hỏi phổ biến)
{full_stats_str}

Nhiệm vụ của bạn:
1. Dựa vào bảng dữ liệu trên để trả lời các câu hỏi về ROI, số giao dịch.
2. NẾU người dùng hỏi một câu hỏi ĐẶC BIỆT yêu cầu truy vấn DỮ LIỆU THÔ (Ví dụ: "Căn nhà đắt nhất giá bao nhiêu?", "Có bao nhiêu nhà bán dưới 500 ngàn đô?"):
   - Bạn có thể viết code Python pandas để truy vấn bản copy của dữ liệu (biến df_ai).
   - HÃY ĐẶT ĐOẠN CODE ĐÓ VÀO GIỮA THẺ <python> và </python>.
   - Ví dụ: <python>df_ai['sale_price'].max()</python>
   - Chỉ được viết MỘT BIỂU THỨC (expression) duy nhất, KHÔNG gán biến.
   - Hệ thống sẽ chạy đoạn code này và trả về kết quả cho bạn để bạn trả lời người dùng.
3. Nếu không cần tính toán nâng cao, hãy trả lời bình thường.
"""'''
text = text.replace(old_sys, new_sys)

# Replace the chat send part
old_chat = '''                            chat = model.start_chat(history=history)
                            response = chat.send_message(prompt)
                            
                            st.markdown(response.text)
                            st.session_state.chat_history.append({"role": "assistant", "content": response.text})'''

new_chat = '''                            chat = model.start_chat(history=history)
                            response = chat.send_message(prompt)
                            
                            # ReAct Loop: Kiểm tra xem AI có muốn chạy code không
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
                                        
                            st.markdown(response.text)
                            st.session_state.chat_history.append({"role": "assistant", "content": response.text})'''

text = text.replace(old_chat, new_chat)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)