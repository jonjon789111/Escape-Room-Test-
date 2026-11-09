
def room_design():

    st.markdown("""
    <style>
    .stApp {background:#101827;}
    .block-container {max-width:1100px;padding-top:2rem;}
    .room-title {
        color:#F4F1EA; text-align:center;
        font-family:Cinzel,serif; font-size:45px;
        letter-spacing:4px; font-weight:bold;
    }
    .room-subtitle {
        color:#C6B78E; text-align:center;
        font-family:'Cormorant Garamond',serif; font-size:22px;
    }
    .gold-line {
        width:75%; height:1px; margin:25px auto;
        background:linear-gradient(to right,transparent,#B59A60,transparent);
    }
    .question-label {
        color:#D8B96F; font-family:Cinzel,serif;
        letter-spacing:3px; font-size:15px;
    }
    div[data-testid="stButton"] button {
        height:48px; border-radius:8px;
        font-family:Cinzel,serif; letter-spacing:2px;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background:#476B56 !important;color:white !important;
        border:1px solid #78947E !important;
    }
    div[data-testid="stButton"] button[kind="secondary"] {
        background:#B59A60 !important;color:#17202B !important;
        border:1px solid #D9C28C !important;
    }
    </style>
    """, unsafe_allow_html=True)


def show_room(title, subtitle, questions, room_number):

    room_design()

    st.markdown(f"""
        <div class="question-label" style="text-align:center">
            ROOM 0{room_number}
        </div>
        <div class="room-title">{title}</div>
        <div class="room-subtitle">{subtitle}</div>
        <div class="gold-line"></div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("LIVES", st.session_state.lives)

    with col2:
        st.metric("HINTS", st.session_state.hints)

    with col3:
        live_timer()

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    number = st.session_state.question_number
    q = questions[number]

    with st.container(border=True):

        st.markdown(
            f'<div class="question-label">CHALLENGE {number + 1} OF 3</div>',
            unsafe_allow_html=True
        )

        st.write(q["question"])
        st.latex(q["formula"])

        answer = st.text_input(
            "YOUR ANSWER",
            key=f"room{room_number}_answer_{number}"
        )

        if st.button("SUBMIT ANSWER", type="primary",
                     use_container_width=True):

            if answer.strip() == q["answer"]:
                st.session_state.feedback = "correct"
            else:
                wrong_answer()
                st.session_state.feedback = "wrong"

            st.rerun()

        if st.button("USE HINT", type="secondary",
                     use_container_width=True):
            use_hint(q["hint"])
            st.rerun()

        if st.session_state.hint_message:
            st.info(st.session_state.hint_message)

        if st.session_state.feedback == "correct":
            st.success("Correct! Challenge completed.")

            if st.button("CONTINUE", type="primary"):
                st.session_state.question_number += 1
                st.session_state.feedback = ""
                st.session_state.hint_message = ""
                st.session_state.hint_used_this_question = False

                if st.session_state.question_number == 3:
                    if room_number == 1:
                        st.session_state.room1_cleared = True
                        st.session_state.question_number = 0
                        st.session_state.page = "room2"

                st.rerun()

        elif st.session_state.feedback == "wrong":
            st.error("Incorrect! One life and five seconds deducted.")
            st.session_state.feedback = ""

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)


# ==========================================
# ROOM 1 — THE BLACKBOARD
# ==========================================

def room1():

    questions = [
        {
            "question": "Find the limit:",
            "formula": r"\lim_{x\to2}(3x+4)",
            "answer": "10",
            "hint": "Substitute x = 2."
        },
        {
            "question": "Evaluate the limit:",
            "formula": r"\lim_{x\to2}\frac{x^2-4}{x-2}",
            "answer": "4",
            "hint": "Factor the numerator."
        },
        {
            "question": "Find the limit:",
            "formula": r"\lim_{x\to1}\frac{x^2+3x-4}{x-1}",
            "answer": "5",
            "hint": "Factor the numerator into (x - 1)(x + 4)."
        }
    ]

    show_room("THE BLACKBOARD", "Limits", questions, 1)


# ==========================================
# ROOM 2 — THE TEACHER'S DESK
# ==========================================

def room2():

    if not st.session_state.room1_cleared:
        st.warning("Complete Room 1 first.")
        return

    questions = [
        {
            "question": "Find the derivative:",
            "formula": r"f(x)=x^4",
            "answer": "4x^3",
            "hint": "Bring the exponent down, then subtract 1."
        },
        {
            "question": "Differentiate:",
            "formula": r"f(x)=5x^3",
            "answer": "15x^2",
            "hint": "Multiply 5 by the exponent 3."
        },
        {
            "question": "Find the derivative:",
            "formula": r"f(x)=3x^5+2x^2",
            "answer": "15x^4+4x",
            "hint": "Differentiate each term separately."
        }
    ]

    show_room("THE TEACHER'S DESK", "Basic Derivatives — Power Rule", questions, 2)
