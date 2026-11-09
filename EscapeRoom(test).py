
import streamlit as st
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="The Locked Classroom",
    page_icon="🔒",
    layout="centered"
)


# ==========================================
# DESIGN AND FONTS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 50% 20%, #17374a 0%, transparent 55%),
        linear-gradient(145deg, #07131d, #102536 55%, #080f17);
    color: #eee6d2;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #e8d3a0 !important;
}

p, label, span {
    font-family: 'Inter', sans-serif;
    color: #eee6d2;
}

.home-small-title {
    font-family: 'Cinzel', serif;
    color: #e7d4a2;
    font-size: 25px;
    font-weight: 600;
    letter-spacing: 8px;
    text-align: center;
    margin-bottom: -10px;
}

.home-main-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(42px, 7vw, 76px);
    font-weight: 800;
    line-height: 1.05;
    text-align: center;
    letter-spacing: 2px;
    color: #f0d99f;
    text-shadow: 0 2px 2px #4d3518,
                 0 4px 12px rgba(226, 184, 100, 0.35);
    margin: 0;
}

.home-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 35px;
    font-weight: 600;
    color: #e6d3a6;
    text-align: center;
    margin-top: 8px;
    letter-spacing: 2px;
}

.gold-line {
    width: 150px;
    height: 2px;
    margin: 22px auto 30px auto;
    background: linear-gradient(90deg, transparent, #d7b66f, transparent);
}

.stButton > button {
    width: 100%;
    min-height: 58px;
    border-radius: 40px;
    border: 1px solid #d4b879;
    background: linear-gradient(135deg, #18364b, #0b1c2a);
    color: #f0dba8;
    font-family: 'Cinzel', serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 2px;
    box-shadow: 0 0 8px rgba(217, 184, 112, 0.15);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #31536a, #142b3d);
    color: #fff0c8;
    border: 1px solid #f5d895;
    box-shadow: 0 0 18px rgba(224, 190, 115, 0.4);
    transform: translateY(-3px);
}

.objective-panel {
    background: rgba(13, 29, 41, 0.78);
    border: 1px solid rgba(181, 194, 195, 0.55);
    border-radius: 20px;
    padding: 25px 30px;
    margin-top: 25px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

.objective-title {
    font-family: 'Cinzel', serif;
    color: #e7d19d;
    font-size: 23px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.objective-text {
    font-family: 'Inter', sans-serif;
    color: #f1eee8;
    font-size: 16px;
    line-height: 1.8;
}

.stTextInput input {
    background-color: #102536;
    color: white;
    border: 1px solid #b99b60;
    border-radius: 8px;
}

hr {
    border-color: rgba(205, 176, 115, 0.35);
}

[data-testid="stMetric"] {
    background: rgba(15, 35, 49, 0.75);
    padding: 12px;
    border: 1px solid rgba(197, 166, 103, 0.4);
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #d9c28f !important;
}

[data-testid="stMetricValue"] {
    color: #f4e5c2 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "lives" not in st.session_state:
    st.session_state.lives = 3

if "hints" not in st.session_state:
    st.session_state.hints = 2

if "time_limit" not in st.session_state:
    st.session_state.time_limit = 600

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "room1_cleared" not in st.session_state:
    st.session_state.room1_cleared = False

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "hint_message" not in st.session_state:
    st.session_state.hint_message = ""

if "hint_used_this_question" not in st.session_state:
    st.session_state.hint_used_this_question = False


# ==========================================
# GAME FUNCTIONS
# ==========================================

def reset_game():

    st.session_state.lives = 3
    st.session_state.hints = 2

    st.session_state.time_limit = 600
    st.session_state.start_time = None

    st.session_state.question_number = 1

    st.session_state.room1_cleared = False
    st.session_state.game_over = False

    st.session_state.feedback = ""
    st.session_state.hint_message = ""

    st.session_state.hint_used_this_question = False

    st.session_state.page = "home"


def start_game():

    st.session_state.start_time = time.time()

    st.session_state.lives = 3
    st.session_state.hints = 2

    st.session_state.question_number = 1

    st.session_state.room1_cleared = False
    st.session_state.game_over = False

    st.session_state.feedback = ""
    st.session_state.hint_message = ""

    st.session_state.hint_used_this_question = False

    st.session_state.page = "room1"


def wrong_answer():

    st.session_state.lives -= 1

    # Deduct 5 seconds

    if st.session_state.start_time is not None:
        st.session_state.start_time -= 5

    st.session_state.feedback = (
        "Incorrect answer! You lost 1 life and 5 seconds."
    )

    if st.session_state.lives <= 0:
        st.session_state.game_over = True


def use_hint(message):

    if st.session_state.hint_used_this_question:

        st.session_state.hint_message = (
            "You have already used a hint for this challenge. "
            "Only 1 hint is allowed per challenge."
        )

    elif st.session_state.hints <= 0:

        st.session_state.hint_message = (
            "You have no hints remaining."
        )

    else:

        st.session_state.hints -= 1

        st.session_state.hint_used_this_question = True

        st.session_state.hint_message = message


# ==========================================
# LIVE TIMER
# ==========================================

@st.fragment(run_every="1s")
def live_timer():

    if st.session_state.start_time is None:
        return

    elapsed_time = time.time() - st.session_state.start_time

    time_left = st.session_state.time_limit - int(elapsed_time)

    if time_left <= 0:

        st.session_state.game_over = True
        st.error("TIME'S UP!")

        st.rerun()

    minutes = time_left // 60
    seconds = time_left % 60

    st.metric(
        label="TIME LEFT",
        value=f"{minutes:02d}:{seconds:02d}"
    )


# ==========================================
# HOME PAGE FUNCTION
# ==========================================

def home_page():

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='home-small-title'>THE</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='home-main-title'>"
        "LOCKED<br>CLASSROOM"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='home-subtitle'>Calculus Escape</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='gold-line'></div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        if st.button("PLAY", key="home_play"):

            st.session_state.page = "story"
            st.rerun()

    with col3:

        if st.button("HOW TO PLAY", key="home_how"):

            st.session_state.page = "instructions"
            st.rerun()

    st.markdown("""
    <div class="objective-panel">

        <div class="objective-title">
            OBJECTIVE
        </div>

        <div class="objective-text">
            Solve Differential Calculus challenges to escape
            four rooms.<br>
            Can you escape before time runs out?
        </div>

    </div>
    """, unsafe_allow_html=True)


# ==========================================
# STORY PAGE FUNCTION
# ==========================================

def story_page():

    st.title("THE STORY")

    st.write(
        "It is already late, and you are the last student "
        "inside the classroom."
    )

    st.write(
        "As you prepare to leave, you discover that the classroom "
        "door is locked. The only way out is to solve the challenges "
        "hidden throughout the room."
    )

    st.write(
        "Four areas stand between you and freedom. "
        "Each area contains three Differential Calculus challenges."
    )

    st.warning("You have only 10 minutes. Think carefully.")

    if st.button("START GAME"):

        start_game()
        st.rerun()

    if st.button("BACK TO MENU"):

        st.session_state.page = "home"
        st.rerun()


# ==========================================
# INSTRUCTIONS PAGE FUNCTION
# ==========================================

def instructions_page():

    st.title("HOW TO PLAY")

    st.subheader("Your Objective")

    st.write(
        "Solve all the challenges in each room to collect keys "
        "and unlock the next area."
    )

    st.subheader("Game Rules")

    st.write("❤️ You have 3 lives.")
    st.write("⏱️ You have 10 minutes to finish the game.")
    st.write("💡 You have 2 hints for the entire game.")
    st.write("🔑 Each room has 3 challenges.")
    st.write("✅ Correct answers allow you to progress.")
    st.write("❌ Wrong answers deduct 1 life and 5 seconds.")
    st.write("💡 Only 1 hint can be used per challenge.")
    st.write(
        "🚪 Lose all your lives or run out of time, "
        "and the game ends."
    )

    st.subheader("Hint System")

    st.write(
        "Hints reveal a step in the solution without showing "
        "the final answer."
    )

    if st.button("BACK TO MENU"):

        st.session_state.page = "home"
        st.rerun()


# ==========================================
# ROOM 1 FUNCTION: THE BLACKBOARD
# ==========================================

def room1():

    st.title("THE LOCKED CLASSROOM")

    st.caption("ROOM 1 / 4")

    st.divider()

    # GAME STATUS

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("LIVES", f"❤️ {st.session_state.lives}")

    with col2:
        live_timer()

    with col3:
        st.metric("HINTS", f"💡 {st.session_state.hints}")

    st.divider()

    # GAME OVER

    if st.session_state.game_over:

        st.error("GAME OVER")

        st.write(
            "You failed to escape the classroom. "
            "Try again and manage your time carefully."
        )

        if st.button("RESTART GAME"):

            reset_game()
            st.rerun()

    # ROOM CLEARED

    elif st.session_state.room1_cleared:

        st.success("ROOM CLEARED!")

        st.title("🔑 FIRST KEY OBTAINED")

        st.write(
            "You successfully solved all three challenges "
            "on the blackboard."
        )

        st.write("The Teacher's Desk is now unlocked.")

        if st.button("CONTINUE"):

            st.session_state.page = "room2"
            st.rerun()

    # ACTIVE CHALLENGES

    else:

        st.subheader("ROOM 1: THE BLACKBOARD")

        st.write(
            "The blackboard contains three mathematical challenges. "
            "Solve each one to unlock the first key."
        )

        st.markdown("### 🔒 Blackboard Challenge")

        # QUESTION 1

        if st.session_state.question_number == 1:

            st.caption("CHALLENGE 1 / 3")

            st.write("Evaluate the following limit:")

            st.latex(r"\lim_{x \to 2}(3x+4)")

            answer = st.text_input(
                "Enter your answer:",
                key="answer_1"
            )

            if st.button("SUBMIT ANSWER", key="submit_1"):

                if answer.strip() == "10":

                    st.session_state.question_number = 2

                    st.session_state.hint_used_this_question = False

                    st.session_state.feedback = ""
                    st.session_state.hint_message = ""

                    st.rerun()

                else:

                    wrong_answer()
                    st.rerun()

            if st.button("USE HINT", key="hint_1"):

                use_hint(
                    "Substitute x = 2 into the expression."
                )

                st.rerun()

        # QUESTION 2

        elif st.session_state.question_number == 2:

            st.caption("CHALLENGE 2 / 3")

            st.write("Evaluate the following limit:")

            st.latex(
                r"\lim_{x \to 2}\frac{x^2-4}{x-2}"
            )

            answer = st.text_input(
                "Enter your answer:",
                key="answer_2"
            )

            if st.button("SUBMIT ANSWER", key="submit_2"):

                if answer.strip() == "4":

                    st.session_state.question_number = 3

                    st.session_state.hint_used_this_question = False

                    st.session_state.feedback = ""
                    st.session_state.hint_message = ""

                    st.rerun()

                else:

                    wrong_answer()
                    st.rerun()

            if st.button("USE HINT", key="hint_2"):

                use_hint(
                    "Factor x² - 4 into (x - 2)(x + 2)."
                )

                st.rerun()

        # QUESTION 3

        elif st.session_state.question_number == 3:

            st.caption("CHALLENGE 3 / 3")

            st.write("Evaluate the following limit:")

            st.latex(
                r"\lim_{x \to 1}\frac{x^2+3x-4}{x-1}"
            )

            answer = st.text_input(
                "Enter your answer:",
                key="answer_3"
            )

            if st.button("SUBMIT ANSWER", key="submit_3"):

                if answer.strip() == "5":

                    st.session_state.room1_cleared = True

                    st.session_state.feedback = ""
                    st.session_state.hint_message = ""

                    st.rerun()

                else:

                    wrong_answer()
                    st.rerun()

            if st.button("USE HINT", key="hint_3"):

                use_hint(
                    "Factor the numerator into (x - 1)(x + 4)."
                )

                st.rerun()

        # FEEDBACK

        if st.session_state.feedback:
            st.error(st.session_state.feedback)

        if st.session_state.hint_message:
            st.info(st.session_state.hint_message)

        # ROOM STATUS

        st.divider()

        st.subheader("ROOM STATUS")

        st.write("🔓 Blackboard: Available")
        st.write("🔒 Teacher's Desk: Locked")
        st.write("🔒 Storage Cabinet: Locked")
        st.write("🔒 Exit Door: Locked")


# ==========================================
# ROOM 2 FUNCTION: THE TEACHER'S DESK
# ==========================================

def room2():

    st.title("ROOM 2: THE TEACHER'S DESK")

    st.caption("ROOM 2 / 4")

    st.divider()

    st.info(
        "Room 2 gameplay has not been added yet."
    )

    if st.button("BACK TO MAIN MENU"):

        st.session_state.page = "home"
        st.rerun()


# ==========================================
# MAIN PAGE NAVIGATION
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
