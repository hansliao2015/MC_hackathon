import streamlit as st

with st.chat_message("user"):
    st.write("Hi 👋，介紹一下你自己？")

# 另一種寫法
message = st.chat_message("assistant")  # 或者寫 "ai"
# message = st.chat_message("assistant", avatar="🦖")  # 自訂頭像
message.write("你好！我是 ChatBot 🤖，可以提供新竹交通相關的資訊！")
message.write("有什麼我可以幫助你的嗎？")

st.chat_input("Say something...")