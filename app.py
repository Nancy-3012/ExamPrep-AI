import streamlit as st
import json
import os
import sys
import random

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ---------------- UI ----------------
st.markdown("""
<style>
.stApp { background-color: #0e0e0e; color: white; }
section[data-testid="stSidebar"] { background-color: #121212; }

.card {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 10px;
    margin-bottom: 12px;
}

.metric-card {
    background: linear-gradient(135deg,#1db954,#191414);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
defaults = {
    "logged_in": False,
    "page": "login",
    "current_page": "Dashboard",
    "generated": False,
    "doc_count": 0,
    "question_count": 0,
    "quiz_count": 0,
    "show_answers": False
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

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

# ---------------- LOGIN ----------------
def login_page():
    st.title("ExamPrep AI")

    if st.session_state.page == "login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("Create Account"):
            st.session_state.page = "signup"
            st.rerun()

    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            if signup(username, password):
                st.success("Account created")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("User already exists")

        if st.button("Back"):
            st.session_state.page = "login"
            st.rerun()

# ---------------- SIDEBAR ----------------
def sidebar():
    st.sidebar.title("ExamPrep AI")

    if st.sidebar.button("Dashboard"):
        st.session_state.current_page = "Dashboard"

    if st.sidebar.button("Upload"):
        st.session_state.current_page = "Upload"

    if st.session_state.generated:
        st.sidebar.markdown("---")
        if st.sidebar.button("MCQ"):
            st.session_state.current_page = "MCQ"
        if st.sidebar.button("Short"):
            st.session_state.current_page = "Short"
        if st.sidebar.button("Long"):
            st.session_state.current_page = "Long"
        if st.sidebar.button("Quiz"):
            st.session_state.current_page = "Quiz"

    st.sidebar.markdown("---")
    st.session_state.show_answers = st.sidebar.toggle("Show Answers")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- MAIN ----------------
def main_app():
    from src.data_processing.pdf_loader import load_pdf
    from src.data_processing.cleaner import clean_text
    from src.chunking.chunker import TextChunker
    from src.question_generation.generator import QuestionGenerator

    sidebar()
    page = st.session_state.current_page

    # -------- DASHBOARD --------
    if page == "Dashboard":
        st.title("Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.markdown(f'<div class="metric-card">Documents<br><h2>{st.session_state.doc_count}</h2></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="metric-card">Questions<br><h2>{st.session_state.question_count}</h2></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="metric-card">Quizzes<br><h2>{st.session_state.quiz_count}</h2></div>', unsafe_allow_html=True)

    # -------- UPLOAD --------
    elif page == "Upload":
        st.title("Upload and Generate")

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

            if st.button("Generate"):
                context = " ".join(random.sample(chunks, min(5, len(chunks))))

                generator = QuestionGenerator()
                mcq, short, viva = generator.generate_questions(context)

                st.session_state.mcq = mcq[:num_questions]
                st.session_state.short = short[:num_questions]
                st.session_state.viva = viva[:num_questions]

                st.session_state.generated = True
                st.session_state.doc_count += 1
                st.session_state.question_count += num_questions

                st.success("Generated successfully")

    # -------- MCQ --------
    elif page == "MCQ":
        st.title("MCQ Questions")

        for i, q in enumerate(st.session_state.mcq):
            st.markdown(f'<div class="card"><b>Q{i+1}. {q["question"]}</b></div>', unsafe_allow_html=True)

            for idx, opt in enumerate(q["options"]):
                st.write(f"{chr(65+idx)}. {opt}")

            if st.session_state.show_answers:
                st.write(f"Answer: {q['answer']}")

            st.write("---")

    # -------- SHORT --------
    elif page == "Short":
        st.title("Short Answers")
        for i, q in enumerate(st.session_state.short):
            st.markdown(f'<div class="card">{i+1}. {q}</div>', unsafe_allow_html=True)

    # -------- LONG --------
    elif page == "Long":
        st.title("Long Answers")
        for i, q in enumerate(st.session_state.viva):
            st.markdown(f'<div class="card">{i+1}. {q}</div>', unsafe_allow_html=True)

    # -------- QUIZ --------
    elif page == "Quiz":
        st.title("Quiz")

        if "q_index" not in st.session_state:
            st.session_state.q_index = 0
            st.session_state.score = 0

        questions = st.session_state.mcq
        total = len(questions)

        st.progress(st.session_state.q_index / total)

        q = questions[st.session_state.q_index]

        st.markdown(f'<div class="card">{q["question"]}</div>', unsafe_allow_html=True)

        selected = st.radio("Select answer", q["options"], key=st.session_state.q_index)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Next"):
                if selected == q["answer"]:
                    st.session_state.score += 1

                st.session_state.q_index += 1

                if st.session_state.q_index >= total:
                    st.session_state.current_page = "Result"

                st.rerun()

        with col2:
            if st.button("Exit"):
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.current_page = "Dashboard"
                st.rerun()

    # -------- RESULT --------
    elif page == "Result":
        st.title("Result")

        st.write(f"Score: {st.session_state.score}")

        st.write(f"Total Questions: {len(st.session_state.mcq)}")
        st.write(f"Correct Answers: {st.session_state.score}")
        st.write(f"Accuracy: {round((st.session_state.score / len(st.session_state.mcq)) * 100, 2)}%")

        st.session_state.quiz_count += 1

        if st.button("Back to Dashboard"):
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.current_page = "Dashboard"
            st.rerun()

# ---------------- ROUTING ----------------
if not st.session_state.logged_in:
    login_page()
else:
    main_app()