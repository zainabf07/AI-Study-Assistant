import streamlit as st

st.set_page_config(page_title="AI Study Assistant")

st.title("AI Study Assistant")
st.write(
    "Enter a study topic to receive a short explanation, three key points, and two quiz questions."
)

topic = st.text_input("Study topic")

if st.button("Generate"):
    if not topic.strip():
        st.error("Please enter a study topic. Empty topics are not allowed.")
