import streamlit as st

from src.data_processing.pdf_loader import load_pdf
from src.data_processing.cleaner import clean_text
from src.chunking.chunker import chunk_text

st.set_page_config(page_title="ExamPrep AI", layout="centered")

st.title("📘 ExamPrep AI")
st.write("Upload your syllabus or notes and generate exam questions.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

num_questions = st.selectbox("Number of questions",[5,10,15])

generate = st.button("Generate Questions")

if uploaded_file is not None:

    with open("temp.pdf","wb") as f:
        f.write(uploaded_file.read())

    raw_text = load_pdf("temp.pdf")

    cleaned_text = clean_text(raw_text)

    chunks = chunk_text(cleaned_text)

    st.success(f"Document split into {len(chunks)} chunks")