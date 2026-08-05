import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_exc = '''                        except Exception as e:
                            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                            error_msg = f"Xin lỗi, AI gặp lỗi khi xử lý câu hỏi này. Chi tiết lỗi: {e}\\n\\nCác model khả dụng cho API Key của bạn: {', '.join(available_models)}"
                            st.error(error_msg)
                            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})'''

new_exc = '''                        except Exception as e:
                            error_str = str(e)
                            if "429" in error_str or "Quota exceeded" in error_str:
                                error_msg = "⏳ AI đang hoạt động quá công suất! API Key của bạn (bản miễn phí) bị giới hạn số lần hỏi liên tục (15-20 lượt/phút). Vì AI tự động gọi lệnh nhiều vòng để lấy dữ liệu thô nên nó đã vượt mốc này. Bạn vui lòng đợi khoảng 40 giây rồi gửi lại câu hỏi nhé!"
                            else:
                                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                                error_msg = f"Xin lỗi, AI gặp lỗi khi xử lý câu hỏi này. Chi tiết lỗi: {e}\\n\\nCác model khả dụng cho API Key của bạn: {', '.join(available_models)}"
                            st.error(error_msg)
                            # Không lưu lỗi 429 vào lịch sử để người dùng có thể gửi lại dễ dàng
                            if "429" not in error_str and "Quota exceeded" not in error_str:
                                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})'''

text = text.replace(old_exc, new_exc)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)