# app.py
# Main Streamlit application — combines calculator and quiz

import streamlit as st
from calculator import OPERATIONS
from quiz import QUESTIONS

# ── Page configuration ─────────────────────────────────────────────
st.set_page_config(page_title="Python Learning Hub", page_icon="🐍")
st.title("🐍 Python Learning Hub")
st.caption("A hands-on tool for Python beginners")

# ── Navigation ─────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🧮 Smart Calculator", "🧠 Python Quiz"])

# ── Tab 1: Calculator ──────────────────────────────────────────────
with tab1:
    st.header("Smart Calculator")
    st.write("Practice Python arithmetic — including edge cases like division by zero.")

    col1, col2 = st.columns(2)
    with col1:
        num_a = st.number_input("First number (a)", value=0.0, key="a")
    with col2:
        num_b = st.number_input("Second number (b)", value=0.0, key="b")

    operation = st.selectbox("Choose an operation", list(OPERATIONS.keys()))

    if st.button("Calculate"):
        try:
            result = OPERATIONS[operation](num_a, num_b)
            st.success(f"**Result:** {result}")
        except ValueError as e:
            st.error(f"⚠️ Error: {e}")

    with st.expander("📖 View the Python function used"):
        st.code(
            f"# The function called for '{operation}'\n"
            f"import inspect\nfrom calculator import *\n"
            f"print(inspect.getsource({OPERATIONS[operation].__name__}))",
            language="python",
        )

# ── Tab 2: Quiz ────────────────────────────────────────────────────
with tab2:
    st.header("Python Concepts Quiz")
    st.write("Test your knowledge! Select an answer for each question, then submit.")

    score = 0
    answers = {}

    with st.form("quiz_form"):
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"**Q{i + 1}. {q['question']}**")
            answers[i] = st.radio(
                label=f"q{i}",
                options=q["options"],
                label_visibility="collapsed",
                key=f"q{i}",
            )
            st.divider()

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        for i, q in enumerate(QUESTIONS):
            if answers[i] == q["answer"]:
                score += 1
                st.success(f"✅ Q{i + 1}: Correct!")
            else:
                st.error(
                    f"❌ Q{i + 1}: Incorrect. "
                    f"The correct answer is **{q['answer']}**."
                )

        st.markdown("---")
        st.metric(label="Your Score", value=f"{score} / {len(QUESTIONS)}")
        percentage = int((score / len(QUESTIONS)) * 100)
        st.progress(percentage)

        if percentage == 100:
            st.balloons()
            st.success("🎉 Perfect score! Excellent work.")
        elif percentage >= 60:
            st.info("👍 Good effort! Review the questions you missed.")
        else:
            st.warning("📚 Keep practising — you are making progress!")