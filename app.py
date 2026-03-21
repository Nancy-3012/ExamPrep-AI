import streamlit as st
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e0e0e;
    color: white;
}

.stApp {
    background-color: #0e0e0e;
}

section[data-testid="stSidebar"] {
    background-color: #121212;
}

.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
}

.metric-card {
    background: linear-gradient(135deg, #1db954, #191414);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
}

button[kind="primary"] {
    background-color: #1db954;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

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
    st.markdown("<h1 style='text-align:center;'>ExamPrep AI</h1>", unsafe_allow_html=True)

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

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- MAIN APP ----------------
def main_app():
    from src.data_processing.pdf_loader import load_pdf
    from src.data_processing.cleaner import clean_text
    from src.chunking.chunker import TextChunker
    from src.question_generation.generator import QuestionGenerator

    sidebar()
    page = st.session_state.current_page

    # ---------------- DASHBOARD ----------------
    if page == "Dashboard":
        st.title("Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.markdown('<div class="metric-card">Documents<br><h2>1</h2></div>', unsafe_allow_html=True)
        col2.markdown('<div class="metric-card">Questions<br><h2>50</h2></div>', unsafe_allow_html=True)
        col3.markdown('<div class="metric-card">Quizzes<br><h2>2</h2></div>', unsafe_allow_html=True)

    # ---------------- UPLOAD ----------------
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
                context = " ".join(chunks[:5])

                generator = QuestionGenerator()
                mcq, short_answer, viva = generator.generate_questions(context)

                st.session_state.mcq = mcq[:num_questions]
                st.session_state.short = short_answer[:num_questions]
                st.session_state.viva = viva[:num_questions]

                st.session_state.generated = True
                st.success("Generated successfully")

    # ---------------- MCQ ----------------
    elif page == "MCQ":
        st.title("MCQ Questions")

        for q in st.session_state.mcq:
            st.markdown(f'<div class="card">{q["question"]}</div>', unsafe_allow_html=True)

    # ---------------- SHORT ----------------
    elif page == "Short":
        st.title("Short Answer")

        for q in st.session_state.short:
            st.markdown(f'<div class="card">{q}</div>', unsafe_allow_html=True)

    # ---------------- LONG ----------------
    elif page == "Long":
        st.title("Long Answer")

        for q in st.session_state.viva:
            st.markdown(f'<div class="card">{q}</div>', unsafe_allow_html=True)

    # ---------------- QUIZ ----------------
    elif page == "Quiz":
        st.title("Quiz")

        score = 0

        for i, q in enumerate(st.session_state.mcq):
            st.markdown(f'<div class="card">{q["question"]}</div>', unsafe_allow_html=True)

            ans = st.radio("Select", q["options"], key=i)

            if ans == q["answer"]:
                score += 1

        if st.button("Submit"):
            st.success(f"Score: {score}/{len(st.session_state.mcq)}")

# ---------------- ROUTING ----------------
if not st.session_state.logged_in:
    login_page()
else:
    main_app()