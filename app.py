import streamlit as st

st.set_page_config(page_title="ExamPrep AI", layout="centered")

st.title("📘 ExamPrep AI")

st.write("Upload your syllabus or notes and generate exam questions.")

uploaded_file = st.file_uploader("Upload syllabus or notes", type=["pdf","txt"])

num_questions = st.selectbox("Number of questions", [5,10,15])

if st.button("Generate Questions"):
    st.write("Questions will be generated here.")