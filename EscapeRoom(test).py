
import streamlit as st
import time

# ==================================
# PAGE CONFIGURATION
# ==================================

st.set_page_config(
    page_title="The Locked Classroom",
    page_icon="🔒",
    layout="centered"
)

# ==================================
# DARK ACADEMIA DESIGN
# ==================================

st.markdown("""
<style>
.stApp {
    background-color: #10131C;
}

h1 {
    color: #D6B66F;
    text-align: center;
    font-size: 45px;
    font-weight: bold;
}

h2, h3 {
    color: #D6B66F;
}

p {
    color: #E8EAF0;
    text-align: center;
    font-size: 17px;
}

.stButton > button {
    background: linear-gradient(135deg, #B99A56, #D6B66F);
    color: #10131C;
    border: 1px solid #E8CC86;
    border-radius: 12px;
    height: 55px;
    font-size: 17px;
    font-weight: bold;
    letter-spacing: 2px;
    box-shadow: 0px 4px 12px rgba(185, 154, 86, 0.20);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #D6B66F, #F0D99A);
    color: #10131C;
    border: 1px solid #F0D99A;
    transform: translateY(-3px);
}

.stButton > button:active {
    transform: translateY(1px);
}
</style>
""", unsafe_allow_html=True)


# ==================================
# GAME VARIABLES
# ==================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "lives" not in st.session_state:
    st.session_state.lives = 3

if "time_left" not in st.session_state:
    st.session_state.time_left = 600

if "hints" not in st.session_state:
    st.session_state.hints = 2

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "room1_cleared" not in st.session_state:
    st.session_state.room1_cleared = False

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# ==================================
# GAME OVER CHECK
# ==================================

if st.session_state.lives <= 0 or st.session_state.time_left <= 0:
    st.session_state.game_over = True


# ==================================
# MAIN MENU SCREEN
# ==================================

if st.session_state.page == "home":

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.title("THE LOCKED CLASSROOM")

    st.markdown(
        "<p>Four rooms. Twelve challenges. One way out.</p>",
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.info(
        "Solve every Differential Calculus challenge "
        "and unlock the classroom exit before time runs out."
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("▶ PLAY", use_container_width=True):
        st.session_state.page = "story"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📖 HOW TO PLAY", use_container_width=True):
        st.session_state.page = "instructions"
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#7D879B; font-size:12px;'>"
        "A DIFFERENTIAL CALCULUS ESCAPE GAME"
        "</p>",
        unsafe_allow_html=True
    )


# ==================================
# STORY SCREEN
# ==================================

elif st.session_state.page == "story":

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.title("THE STORY")

    st.markdown("---")

    st.markdown("""
    You stayed late at school to finish your work.

    After spending hours solving problems, you finally
    decided it was time to go home.

    But when you reached the classroom door...

    **It was locked.**

    You tried opening it, but it wouldn't budge.
    You looked around and noticed something strange.

    The classroom was divided into four different areas.
    Each area contained puzzles, locked compartments,
    and mysterious challenges.

    A note on the teacher's desk caught your attention:

    *"To escape this classroom, you must prove your
    knowledge. Solve the challenges, collect the keys,
    and unlock the final exit."*

    You realized that the only way out was through
    Differential Calculus.

    The clock is ticking.

    **Can you solve all the challenges and escape
    before time runs out?**
    """)

    st.markdown("---")

    st.info("Four rooms. Twelve challenges. One way out.")

    if st.button("🔒 START GAME", use_container_width=True):

        # RESET GAME
        st.session_state.lives = 3
        st.session_state.time_left = 600
        st.session_state.hints = 2
        st.session_state.question_number = 1
        st.session_state.room1_cleared = False
        st.session_state.game_over = False

        st.session_state.page = "room1"
        st.rerun()

    if st.button("⬅ BACK TO MAIN MENU", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()


# ==================================
# HOW TO PLAY SCREEN
# ==================================

elif st.session_state.page == "instructions":

    st.markdown("<br>", unsafe_allow_html=True)

    st.title("HOW TO PLAY")

    st.markdown(
        "<p>Learn the rules before entering the classroom!</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("🎯 OBJECTIVE")

    st.write(
        "Escape the locked classroom by completing "
        "all 12 Differential Calculus challenges "
        "across four rooms."
    )

    st.markdown("---")

    st.subheader("🔑 GAME PROGRESSION")

    st.write("""
    1. Start in Room 1 and solve its three challenges.
    2. Complete all three challenges to earn a key.
    3. Use the key to unlock the next room.
    4. Complete all four rooms to escape.
    """)

    st.markdown("---")

    st.subheader("❤️ LIVES")

    st.write("""
    - You start with 3 lives.
    - Every incorrect answer costs 1 life.
    - Lose all 3 lives and the game ends.
    """)

    st.markdown("---")

    st.subheader("⏱️ TIMER")

    st.write("""
    - You have 10 minutes to escape.
    - Every incorrect answer deducts 5 seconds.
    - If the timer reaches zero, the game ends.
    """)

    st.markdown("---")

    st.subheader("💡 HINTS")

    st.write("""
    - You have 2 hints for the entire game.
    - Each hint reveals one step toward the solution.
    - Hints will not reveal the final answer.
    """)

    st.markdown("---")

    st.subheader("📌 IMPORTANT RULES")

    st.write("""
    - Complete challenges in the correct order.
    - Correct answers allow you to proceed.
    - Incorrect answers cost a life and 5 seconds.
    - You can retry a question after an incorrect answer.
    - Your lives, timer, and hints carry over between rooms.
    """)

    st.markdown("---")

    st.success(
        "YOUR MISSION: Solve all 12 challenges, "
        "collect all 3 keys, and escape before time runs out!"
    )

    if st.button("⬅ BACK TO MAIN MENU", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()


# ==================================
# ROOM 1 - THE BLACKBOARD
# ==================================

elif st.session_state.page == "room1":

    st.markdown("<br>", unsafe_allow_html=True)

    st.title("THE LOCKED CLASSROOM")

    st.subheader("ROOM 1: THE BLACKBOARD")

    st.write(
        "Three challenges are written on the blackboard. "
        "Solve them to discover the First Key."
    )

    st.markdown("---")

    # PLAYER STATUS

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("❤️ Lives", st.session_state.lives)

    with col2:
        st.metric("⏱️ Time", st.session_state.time_left)

    with col3:
        st.metric("💡 Hints", st.session_state.hints)

    st.markdown("---")

    # GAME OVER

    if st.session_state.game_over:

        st.error("GAME OVER!")

        st.write("You ran out of lives or time.")

        if st.button("RESTART GAME"):
            st.session_state.lives = 3
            st.session_state.time_left = 600
            st.session_state.hints = 2
            st.session_state.question_number = 1
            st.session_state.room1_cleared = False
            st.session_state.game_over = False
            st.rerun()

    # ROOM COMPLETION

    elif st.session_state.room1_cleared:

        st.success("ROOM 1 CLEARED!")

        st.title("🔑 FIRST KEY FOUND!")

        st.write(
            "You successfully solved all three "
            "blackboard challenges."
        )

        st.info("The Teacher's Desk is now unlocked!")

        if st.button("CONTINUE"):
            st.session_state.page = "room2"
            st.rerun()

    # CHALLENGE 1

    elif st.session_state.question_number == 1:

        st.subheader("CHALLENGE 1: DIRECT SUBSTITUTION")

        st.write("Evaluate the following limit:")

        st.latex(r"\lim_{x \to 2}(3x+4)")

        answer = st.text_input(
            "Enter your answer:",
            key="room1_answer1"
        )

        if st.button("SUBMIT ANSWER", key="submit1"):

            if answer.strip() == "10":

                st.success("Correct! Challenge 1 completed.")

                st.session_state.question_number = 2
                st.rerun()

            else:

                st.session_state.lives -= 1
                st.session_state.time_left -= 5

                st.error("Wrong answer! You lost one life and 5 seconds.")

                if st.session_state.lives <= 0:
                    st.session_state.game_over = True

                st.rerun()

    # CHALLENGE 2

    elif st.session_state.question_number == 2:

        st.subheader("CHALLENGE 2: FACTORING")

        st.write("Evaluate the following limit:")

        st.latex(r"\lim_{x \to 2}\frac{x^2-4}{x-2}")

        answer = st.text_input(
            "Enter your answer:",
            key="room1_answer2"
        )

        if st.button("SUBMIT ANSWER", key="submit2"):

            if answer.strip() == "4":

                st.success("Correct! Challenge 2 completed.")

                st.session_state.question_number = 3
                st.rerun()

            else:

                st.session_state.lives -= 1
                st.session_state.time_left -= 5

                st.error("Wrong answer! You lost one life and 5 seconds.")

                if st.session_state.lives <= 0:
                    st.session_state.game_over = True

                st.rerun()

    # CHALLENGE 3

    elif st.session_state.question_number == 3:

        st.subheader("CHALLENGE 3: RATIONAL LIMITS")

        st.write("Evaluate the following limit:")

        st.latex(r"\lim_{x \to 1}\frac{x^2+3x-4}{x-1}")

        answer = st.text_input(
            "Enter your answer:",
            key="room1_answer3"
        )

        if st.button("SUBMIT ANSWER", key="submit3"):

            if answer.strip() == "5":

                st.success("Correct! You completed all challenges!")

                st.session_state.question_number = 4
                st.session_state.room1_cleared = True

                st.rerun()

            else:

                st.session_state.lives -= 1
                st.session_state.time_left -= 5

                st.error("Wrong answer! You lost one life and 5 seconds.")

                if st.session_state.lives <= 0:
                    st.session_state.game_over = True

                st.rerun()

    # HINT SYSTEM

    if not st.session_state.game_over and not st.session_state.room1_cleared:

        st.markdown("---")

        if st.button("💡 USE HINT", use_container_width=True):

            if st.session_state.hints > 0:

                if st.session_state.question_number == 1:
                    st.info("Hint: Substitute x = 2 into 3x + 4.")

                elif st.session_state.question_number == 2:
                    st.info("Hint: Factor x² - 4 into (x - 2)(x + 2).")

                elif st.session_state.question_number == 3:
                    st.info("Hint: Factor the numerator into (x - 1)(x + 4).")

                st.session_state.hints -= 1

                st.rerun()

            else:
                st.warning("You have no hints remaining.")

    # BACK BUTTON

    st.markdown("---")

    if st.button("⬅ BACK TO MAIN MENU"):
        st.session_state.page = "home"
        st.rerun()
