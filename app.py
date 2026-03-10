import streamlit as st

st.title("ExamPrep AI")

st.write("Upload your syllabus or notes and generate exam questions.")

uploaded_file = st.file_uploader("Upload syllabus or notes")

num_questions = st.selectbox(
    "Select number of questions",
    [5,10,15]
)

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    st.write("File name:", uploaded_file.name)
    st.write("File type:", uploaded_file.type)

if st.button("Generate Questions"):
    st.write("Questions will appear here.")