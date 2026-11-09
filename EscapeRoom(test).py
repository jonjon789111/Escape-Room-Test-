
import streamlit as st
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="The Locked Classroom",
    page_icon="🔒",
    layout="wide"
)

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "page": "home",
    "lives": 3,
    "hints": 2,
    "time_limit": 600,
    "start_time": None,
    "question_number": 0,
    "room1_cleared": False,
    "game_over": False,
    "feedback": "",
    "hint_message": "",
    "hint_used_this_question": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# SHARED DESIGN
# ==========================================

def design():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;800&family=Cormorant+Garamond:wght@400;500;600&display=swap');

    .stApp {
        background: #101827;
        color: #F4F1EA;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-family: Cinzel, serif;
        font-size: clamp(40px, 5vw, 68px);
        font-weight: 800;
        letter-spacing: 5px;
        color: #F4F1EA;
        text-align: center;
    }

    .subtitle {
        font-family: 'Cormorant Garamond', serif;
        font-size: 24px;
        color: #C6B78E;
        text-align: center;
    }

    .gold-line {
        width: 75%;
        height: 1px;
        margin: 25px auto;
        background: linear-gradient(to right, transparent, #B59A60, transparent);
    }

    .section-title {
        font-family: Cinzel, serif;
        color: #D8B96F;
        font-size: 18px;
        letter-spacing: 3px;
    }

    .story-text {
        font-family: 'Cormorant Garamond', serif;
        color: #E0E3E8;
        font-size: 21px;
        line-height: 1.7;
    }

    div[data-testid="stButton"] button {
        height: 52px;
        border-radius: 8px;
        font-family: Cinzel, serif;
        font-weight: bold;
        letter-spacing: 2px;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: #476B56 !important;
        color: white !important;
        border: 1px solid #78947E !important;
    }

    div[data-testid="stButton"] button[kind="secondary"] {
        background: #B59A60 !important;
        color: #17202B !important;
        border: 1px solid #D9C28C !important;
    }

    </style>
    """, unsafe_allow_html=True)


def header(label, title, subtitle):

    st.markdown(f"""
        <div class="section-title" style="text-align:center">{label}</div>
        <div class="main-title">{title}</div>
        <div class="subtitle">{subtitle}</div>
        <div class="gold-line"></div>
    """, unsafe_allow_html=True)


# ==========================================
# GAME FUNCTIONS
# ==========================================

def reset_game():

    st.session_state.lives = 3
    st.session_state.hints = 2
    st.session_state.time_limit = 600
    st.session_state.start_time = None
    st.session_state.question_number = 0
    st.session_state.room1_cleared = False
    st.session_state.game_over = False
    st.session_state.feedback = ""
    st.session_state.hint_message = ""
    st.session_state.hint_used_this_question = False


def start_game():

    reset_game()
    st.session_state.start_time = time.time()
    st.session_state.page = "room1"


def wrong_answer():

    st.session_state.lives -= 1
    st.session_state.start_time -= 5

    if st.session_state.lives <= 0:
        st.session_state.game_over = True


def use_hint(message):

    if st.session_state.hint_used_this_question:
        st.warning("You already used a hint for this question.")
    elif st.session_state.hints > 0:
        st.session_state.hints -= 1
        st.session_state.hint_used_this_question = True
        st.session_state.hint_message = message
    else:
        st.warning("No hints remaining.")


@st.fragment(run_every="1s")
def live_timer():

    if st.session_state.start_time is None:
        return

    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(st.session_state.time_limit - elapsed))

    minutes, seconds = divmod(remaining, 60)
    st.metric("TIME", f"{minutes:02d}:{seconds:02d}")

    if remaining <= 0:
        st.session_state.game_over = True
        st.rerun()


# ==========================================
# HOMEPAGE
# ==========================================

def home_page():

    design()

    st.write("")
    st.write("")

    st.markdown("""
        <div class="main-title">THE LOCKED CLASSROOM</div>
        <div class="subtitle">A Differential Calculus Escape Game</div>
        <div class="subtitle" style="font-size:18px;letter-spacing:3px">
            FOUR ROOMS. TWELVE CHALLENGES. ONE WAY OUT.
        </div>
        <div class="gold-line"></div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 5, 1])

    with center:
        with st.container(border=True):
            st.markdown(
                '<div class="section-title" style="text-align:center">OBJECTIVE</div>',
                unsafe_allow_html=True
            )
            st.write("")
            st.markdown(
                '<div class="story-text" style="text-align:center">'
                'Solve Differential Calculus challenges to escape the locked classroom.'
                '<br>Can you complete all four rooms before time runs out?'
                '</div>',
                unsafe_allow_html=True
            )

    st.write("")
    left, play, gap, instructions, right = st.columns(
        [1.5, 2.5, 0.3, 2.5, 1.5]
    )

    with play:
        if st.button("PLAY", type="primary", use_container_width=True):
            st.session_state.page = "story"
            st.rerun()

    with instructions:
        if st.button("HOW TO PLAY", type="secondary", use_container_width=True):
            st.session_state.page = "instructions"
            st.rerun()

    st.markdown(
        '<div class="subtitle" style="font-size:17px;margin-top:40px">'
        'THINK CAREFULLY. SOLVE WISELY. ESCAPE.'
        '</div>',
        unsafe_allow_html=True
    )


# ==========================================
# STORY PAGE
# ==========================================

def story_page():
    design()

    st.markdown("")
    st.markdown("## 📖 THE STORY")
    st.caption("THE LOCKED CLASSROOM  |  AN ESCAPE ROOM ADVENTURE")
    st.divider()

    st.markdown("### THE FINAL BELL HAS RUNG...")

    st.write(
        "As you prepare to leave, you reach for the door. "
        "But something is wrong. **It's locked.**"
    )

    st.write("")

    st.info(
        "Suddenly, strange mathematical challenges begin appearing "
        "around the classroom."
    )

    st.markdown("### FOUR AREAS. FOUR CHALLENGES.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown("### 🖍️ The Blackboard")
            st.caption("Where the first clues await.")

        with st.container(border=True):
            st.markdown("### 🗄️ The Storage Cabinet")
            st.caption("A collection of difficult challenges.")

    with col2:
        with st.container(border=True):
            st.markdown("### 🪑 The Teacher's Desk")
            st.caption("More than just an ordinary desk.")

        with st.container(border=True):
            st.markdown("### 🚪 The Exit Door")
            st.caption("Your final obstacle to freedom.")

    st.write("")

    st.warning(
        "You must explore all four areas, solve every challenge, "
        "and collect the keys to escape."
    )

    st.markdown("### BUT REMEMBER...")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("LIVES", "3")
        st.caption("Every wrong answer costs one life.")

    with col2:
        st.metric("TIME PENALTY", "5 seconds")
        st.caption("Every mistake takes away precious time.")

    st.divider()

    st.markdown("### YOUR MISSION")

    st.markdown(
        "**Solve the problems. Collect the keys. Escape the classroom.**"
    )

    st.write("")

    left, right = st.columns(2)

    with left:
        if st.button("← BACK TO MENU", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    with right:
        if st.button(
            "START GAME →",
            type="primary",
            use_container_width=True
        ):
            start_game()
            st.rerun()

# ==========================================
# INSTRUCTIONS PAGE
# ==========================================

def instructions_page():

    design()
    header("THE LOCKED CLASSROOM", "HOW TO PLAY",
           "Read carefully before entering.")

    left, center, right = st.columns([1, 5, 1])

    with center:

        with st.container(border=True):
            st.markdown('<div class="section-title">YOUR OBJECTIVE</div>',
                        unsafe_allow_html=True)
            st.markdown("""
            <div class="story-text">
                Complete all four rooms by answering three
                Differential Calculus questions in each room.
                Solve every challenge to unlock your way out.
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown(
        '<div class="section-title" style="text-align:center">GAME RULES</div>',
        unsafe_allow_html=True
    )
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("""
            <div class="story-text">
            <b style="color:#D8B96F">01 — FOUR ROOMS</b><br>
            Complete three questions in each room.<br><br>

            <b style="color:#D8B96F">02 — THREE LIVES</b><br>
            Every incorrect answer costs one life.<br><br>

            <b style="color:#D8B96F">03 — TIME LIMIT</b><br>
            You have ten minutes to escape.
            </div>
            """, unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.markdown("""
            <div class="story-text">
            <b style="color:#D8B96F">04 — TWO HINTS</b><br>
            You have two hints for the entire game.<br><br>

            <b style="color:#D8B96F">05 — TIME PENALTY</b><br>
            Every wrong answer deducts five seconds.<br><br>

            <b style="color:#D8B96F">06 — GAME OVER</b><br>
            The game ends when you run out of lives or time.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title" style="text-align:center">YOUR FOUR DESTINATIONS</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4)

    rooms = [
        ("ROOM 01", "BLACKBOARD", "Limits"),
        ("ROOM 02", "TEACHER'S DESK", "Power Rule"),
        ("ROOM 03", "STORAGE CABINET", "Product, Quotient, Chain Rules"),
        ("ROOM 04", "EXIT DOOR", "Trigonometric Derivatives")
    ]

    for col, room in zip(cols, rooms):
        with col:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="section-title" style="text-align:center">
                        {room[0]}
                    </div>
                    <div class="subtitle" style="font-size:17px">
                        {room[1]}
                    </div>
                    <div class="story-text" style="text-align:center">
                        {room[2]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.write("")
    left, back, gap, start, right = st.columns([1.5, 2.5, 0.3, 2.5, 1.5])

    with back:
        if st.button("BACK TO MENU", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    with start:
        if st.button("START GAME", type="primary", use_container_width=True):
            start_game()
            st.rerun()


# ==========================================
# ROOM 1 — THE BLACKBOARD
# ==========================================

def room1():

    design()
    header("ROOM 01", "THE BLACKBOARD", "The first challenge — Limits")

    if st.session_state.game_over:
        st.error("GAME OVER! You have run out of lives or time.")
        if st.button("RETURN TO MENU"):
            st.session_state.page = "home"
            st.rerun()
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("LIVES", st.session_state.lives)

    with col2:
        st.metric("HINTS", st.session_state.hints)

    with col3:
        live_timer()

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    questions = [
        {
            "question": "Find the limit:",
            "formula": r"\lim_{x\to2}(3x+4)",
            "answer": "10",
            "hint": "Substitute x = 2 into the expression."
        },
        {
            "question": "Evaluate the following limit:",
            "formula": r"\lim_{x\to2}\frac{x^2-4}{x-2}",
            "answer": "4",
            "hint": "Factor the numerator into (x - 2)(x + 2)."
        },
        {
            "question": "Find the limit:",
            "formula": r"\lim_{x\to1}\frac{x^2+3x-4}{x-1}",
            "answer": "5",
            "hint": "Factor the numerator into (x - 1)(x + 4)."
        }
    ]

    number = st.session_state.question_number
    q = questions[number]

    left, center, right = st.columns([1, 5, 1])

    with center:
        with st.container(border=True):

            st.markdown(
                f'<div class="section-title">CHALLENGE {number + 1} OF 3</div>',
                unsafe_allow_html=True
            )

            st.write(q["question"])
            st.latex(q["formula"])

            answer = st.text_input(
                "YOUR ANSWER",
                key=f"room1_answer_{number}"
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
                st.success("Correct! You solved the challenge.")

                if st.button("CONTINUE", type="primary"):
                    st.session_state.question_number += 1
                    st.session_state.feedback = ""
                    st.session_state.hint_message = ""
                    st.session_state.hint_used_this_question = False

                    if st.session_state.question_number == 3:
                        st.session_state.room1_cleared = True
                        st.session_state.question_number = 0
                        st.session_state.page = "room2"

                    st.rerun()

            elif st.session_state.feedback == "wrong":
                st.error("Incorrect! One life and five seconds deducted.")
                st.session_state.feedback = ""

                if st.session_state.game_over:
                    st.rerun()

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)


# ==========================================
# ROOM 2 — THE TEACHER'S DESK
# ==========================================

def room2():

    design()
    header("ROOM 02", "THE TEACHER'S DESK",
           "Basic Derivatives — Power Rule")

    if not st.session_state.room1_cleared:
        st.warning("Complete Room 1 first.")
        return

    if st.session_state.game_over:
        st.error("GAME OVER! You have run out of lives or time.")
        if st.button("RETURN TO MENU"):
            st.session_state.page = "home"
            st.rerun()
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("LIVES", st.session_state.lives)

    with col2:
        st.metric("HINTS", st.session_state.hints)

    with col3:
        live_timer()

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    # ROOM 2 QUESTIONS WILL BE ADDED HERE

    with st.container(border=True):
        st.markdown(
            '<div class="section-title">ROOM 02 UNLOCKED</div>',
            unsafe_allow_html=True
        )
        st.write("The Teacher's Desk is ready for its challenges.")
        st.info("Room 2 questions and gameplay have not been added yet.")


# ==========================================
# PAGE NAVIGATION
# ==========================================

if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "story":
    story_page()

elif st.session_state.page == "instructions":
    instructions_page()

elif st.session_state.page == "room1":
    room1()

elif st.session_state.page == "room2":
    room2()
