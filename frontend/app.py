import streamlit as st
import requests
import os

# Lấy BACKEND_URL từ biến môi trường
BACKEND_URL = os.getenv("BACKEND_URL")

st.title("Chatbot with Gemini API")

# Kiểm tra trạng thái session
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-1.5-flash"  # Model Gemini

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn trước đó
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận đầu vào từ người dùng
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Gửi yêu cầu đến Backend (FastAPI)
        response = requests.post(
            f"{BACKEND_URL}/api/v1/chat",  # Địa chỉ backend API
            json={
                "message": prompt,
                "history": st.session_state.messages,
            },
        )
        
        # Lấy nội dung từ response JSON
        response_data = response.json()  # Giả sử API trả về dữ liệu JSON

        # Hiển thị phản hồi từ Gemini API
        st.markdown(response_data.get("message"))
        
        # Thêm phản hồi vào session state
        st.session_state.messages.append({"role": "assistant", "content": response_data.get("message")})
