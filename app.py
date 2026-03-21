import streamlit as st
import json
import os
import sys

# Fix imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "view" not in st.session_state:
    st.session_state.view = "home"

if "generated" not in st.session_state:
    st.session_state.generated = False

# ---------------- USER STORAGE ----------------
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ---------------- AUTH ----------------
def login(username, password):
    users = load_users()
    return username in users and users[username] == password

def signup(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("ExamPrep AI")

    if st.session_state.page == "login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("Go to Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

    else:
        st.subheader("Sign Up")

        username = st.text_input("Create Username")
        password = st.text_input("Create Password", type="password")

        if st.button("Sign Up"):
            if signup(username, password):
                st.success("Account created. Please login.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Username already exists")

        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()

# ---------------- MAIN APP ----------------
def main_app():
    from src.data_processing.pdf_loader import load_pdf
    from src.data_processing.cleaner import clean_text
    from src.chunking.chunker import TextChunker
    from src.question_generation.generator import QuestionGenerator

    st.title("ExamPrep AI Dashboard")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.view = "home"
        st.rerun()

    # ---------------- HOME SCREEN ----------------
    if st.session_state.view == "home":

        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        num_questions = st.selectbox("Number of questions", [5, 10, 15])

        if uploaded_file:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            raw_text = load_pdf("temp.pdf")
            cleaned_text = clean_text(raw_text)

            chunker = TextChunker()
            chunks = chunker.split_text(cleaned_text)

            st.success(f"{len(chunks)} chunks created")

            if st.button("Generate Questions"):
                context = " ".join(chunks[:5])

                generator = QuestionGenerator()
                mcq, short_answer, viva = generator.generate_questions(context)

                st.session_state.mcq = mcq[:num_questions]
                st.session_state.short = short_answer[:num_questions]
                st.session_state.viva = viva[:num_questions]

                st.session_state.generated = True
                st.success("Questions Generated")

        if st.session_state.generated:
            st.subheader("Select Mode")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("MCQ"):
                    st.session_state.view = "mcq"
                    st.rerun()

                if st.button("Long Answer"):
                    st.session_state.view = "long"
                    st.rerun()

            with col2:
                if st.button("Short Answer"):
                    st.session_state.view = "short"
                    st.rerun()

                if st.button("Quiz"):
                    st.session_state.view = "quiz"
                    st.rerun()

    # ---------------- MCQ PAGE ----------------
    elif st.session_state.view == "mcq":
        st.subheader("MCQ Questions")

        if st.button("Back"):
            st.session_state.view = "home"
            st.rerun()

        for i, q in enumerate(st.session_state.mcq):
            st.write(f"Q{i+1}: {q['question']}")
            for idx, opt in enumerate(q["options"]):
                st.write(f"{chr(65+idx)}) {opt}")
            st.write(f"Answer: {q['answer']}")
            st.write("---")

    # ---------------- SHORT PAGE ----------------
    elif st.session_state.view == "short":
        st.subheader("Short Answer Questions")

        if st.button("Back"):
            st.session_state.view = "home"
            st.rerun()

        for i, q in enumerate(st.session_state.short):
            st.write(f"{i+1}. {q}")

    # ---------------- LONG PAGE ----------------
    elif st.session_state.view == "long":
        st.subheader("Long Answer Questions")

        if st.button("Back"):
            st.session_state.view = "home"
            st.rerun()

        for i, q in enumerate(st.session_state.viva):
            st.write(f"{i+1}. {q}")

    # ---------------- QUIZ PAGE ----------------
    elif st.session_state.view == "quiz":
        st.subheader("Quiz Mode")

        if st.button("Back"):
            st.session_state.view = "home"
            st.rerun()

        score = 0

        for i, q in enumerate(st.session_state.mcq):
            st.write(f"Q{i+1}: {q['question']}")
            answer = st.radio(
                "Select answer",
                q["options"],
                key=f"quiz_{i}"
            )

            if answer == q["answer"]:
                score += 1

        if st.button("Submit Quiz"):
            st.success(f"Your Score: {score}/{len(st.session_state.mcq)}")

# ---------------- ROUTING ----------------
if not st.session_state.logged_in:
    login_page()
else:
    main_app()