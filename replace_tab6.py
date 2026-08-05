import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

tab6_index = -1
for i, l in enumerate(lines):
    if l.startswith('with tab6:'):
        tab6_index = i
        break

if tab6_index != -1:
    new_lines = lines[:tab6_index]
    
    clean_code = '''# ============================================================
# TAB 6 – TRỢ LÝ AI (GEMINI NATIVE)
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
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Tính toán một số thống kê cơ bản từ dataframe để đưa vào ngữ cảnh AI
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
- Các khu vực trong dữ liệu: {neighborhoods_str}

Nhiệm vụ của bạn:
1. Trả lời các câu hỏi phân tích dữ liệu của người dùng một cách ngắn gọn, súc tích và chuyên nghiệp bằng Tiếng Việt.
2. Dựa vào các thông số thống kê tổng quan ở trên để tư vấn hoặc ước lượng.
3. Nếu người dùng hỏi chi tiết ngoài dữ liệu mẫu, hãy giải thích chung về xu hướng thị trường NY hoặc dựa vào kiến thức có sẵn của bạn.
4. KHÔNG cung cấp code Python hoặc SQL. Chỉ đóng vai trò tư vấn viên Bất động sản và phân tích thị trường.
"""
            
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
            # Giao diện Chat
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
                
            # Hiển thị lịch sử
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    
            # Ô nhập câu hỏi
            if prompt := st.chat_input("Hãy hỏi bất cứ điều gì về dữ liệu BĐS này... (VD: Đánh giá tổng quan thị trường?)"):
                # Lưu câu hỏi
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                    
                # Gọi Gemini
                with st.chat_message("assistant"):
                    with st.spinner("🤖 AI đang suy nghĩ và phân tích dữ liệu..."):
                        try:
                            # Chuyển lịch sử sang định dạng Gemini
                            history = []
                            for msg in st.session_state.chat_history[:-1]:
                                role = "user" if msg["role"] == "user" else "model"
                                history.append({"role": role, "parts": [msg["content"]]})
                                
                            chat = model.start_chat(history=history)
                            response = chat.send_message(prompt)
                            
                            st.markdown(response.text)
                            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                        except Exception as e:
                            error_msg = f"Xin lỗi, AI gặp lỗi khi xử lý câu hỏi này. Chi tiết lỗi: {e}"
                            st.error(error_msg)
                            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                            
        except Exception as e:
            import traceback
            st.error(f"Lỗi khởi tạo Trợ lý AI: {type(e).__name__} - {str(e)}")
            st.code(traceback.format_exc())
'''
    new_lines.append(clean_code + '\n')
    
    with io.open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Replaced chunk successfully!")
else:
    print("Could not find start of tab6")