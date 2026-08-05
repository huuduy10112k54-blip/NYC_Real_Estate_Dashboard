import io

with io.open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the exception block in Tab 6
old_exc = '''                        except Exception as e:
                            error_msg = f"Xin lỗi, AI gặp lỗi khi xử lý câu hỏi này. Chi tiết lỗi: {e}"
                            st.error(error_msg)
                            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})'''

new_exc = '''                        except Exception as e:
                            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                            error_msg = f"Xin lỗi, AI gặp lỗi khi xử lý câu hỏi này. Chi tiết lỗi: {e}\\n\\nCác model khả dụng cho API Key của bạn: {', '.join(available_models)}"
                            st.error(error_msg)
                            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})'''

text = text.replace(old_exc, new_exc)

with io.open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)