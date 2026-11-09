
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
# RESET GAME
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


# ==========================================
# START GAME
# ==========================================

def start_game():

    st.session_state.lives = 3
    st.session_state.hints = 2

    st.session_state.time_limit = 600
    st.session_state.start_time = time.time()

    st.session_state.question_number = 1

    st.session_state.room1_cleared = False
    st.session_state.game_over = False

    st.session_state.feedback = ""
    st.session_state.hint_message = ""

    st.session_state.hint_used_this_question = False

    st.session_state.page = "room1"


# ==========================================
# WRONG ANSWER
# ==========================================

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


# ==========================================
# HINT SYSTEM
# ==========================================

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
        st.metric("TIME LEFT", "10:00")
        return

    if st.session_state.game_over:
        st.metric("TIME LEFT", "00:00")
        return

    elapsed_time = time.time() - st.session_state.start_time

    time_left = st.session_state.time_limit - int(elapsed_time)

    if time_left <= 0:

        st.session_state.game_over = True

        st.metric("TIME LEFT", "00:00")

        st.rerun()

    minutes = time_left // 60
    seconds = time_left % 60

    st.metric(
        "TIME LEFT",
        f"{minutes:02d}:{seconds:02d}"
    )


# ==========================================
# HOME PAGE
# ==========================================

def home_page():

    # ==================================
    # TITLE
    # ==================================

    st.write("")
    st.write("")

    st.title("THE LOCKED CLASSROOM")

    st.subheader("A Differential Calculus Escape Game")

    st.write("Four rooms. Twelve challenges. One way out.")

    st.write("")
    st.write("")
    st.divider()

    # ==================================
    # OBJECTIVE
    # ==================================

    with st.container(border=True):

        st.subheader("OBJECTIVE")

        st.write(
            "Solve every Differential Calculus challenge "
            "and unlock the classroom exit before time runs out."
        )

    st.write("")
    st.write("")

    # ==================================
    # BUTTONS
    # ==================================

    play_col, how_col = st.columns(2)

    with play_col:
        if st.button(
            "▶ PLAY",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "story"
            st.rerun()

    with how_col:
        if st.button(
            "📖 HOW TO PLAY",
            type="secondary",
            use_container_width=True
        ):
            st.session_state.page = "instructions"
            st.rerun()

    st.write("")
    st.write("")
    st.divider()

    # ==================================
    # FOOTER
    # ==================================

    st.caption("A DIFFERENTIAL CALCULUS ESCAPE GAME")

# ==========================================
# STORY PAGE
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
# INSTRUCTIONS PAGE
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
# ROOM 1: THE BLACKBOARD
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

        return

    # ROOM CLEARED

    if st.session_state.room1_cleared:

        st.success("ROOM CLEARED!")

        st.title("FIRST KEY OBTAINED")

        st.write(
            "You successfully solved all three challenges "
            "on the blackboard."
        )

        st.write("The Teacher's Desk is now unlocked.")

        if st.button("CONTINUE"):

            st.session_state.page = "room2"
            st.rerun()

        return

    # ACTIVE CHALLENGES

    st.subheader("ROOM 1: THE BLACKBOARD")

    st.write(
        "The blackboard contains three mathematical challenges. "
        "Solve each one to unlock the first key."
    )

    st.divider()

    # --------------------------------------
    # QUESTION 1
    # --------------------------------------

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

    # --------------------------------------
    # QUESTION 2
    # --------------------------------------

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

    # --------------------------------------
    # QUESTION 3
    # --------------------------------------

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

    # --------------------------------------
    # FEEDBACK
    # --------------------------------------

    if st.session_state.feedback:
        st.error(st.session_state.feedback)

    if st.session_state.hint_message:
        st.info(st.session_state.hint_message)

    # --------------------------------------
    # ROOM STATUS
    # --------------------------------------

    st.divider()

    st.subheader("ROOM STATUS")

    st.write("🔓 Blackboard: Available")

    st.write("🔒 Teacher's Desk: Locked")

    st.write("🔒 Storage Cabinet: Locked")

    st.write("🔒 Exit Door: Locked")


# ==========================================
# ROOM 2: THE TEACHER'S DESK
# ==========================================

def room2():

    st.title("ROOM 2: THE TEACHER'S DESK")

    st.caption("ROOM 2 / 4")

    st.divider()

    st.info("Room 2 gameplay has not been added yet.")

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
