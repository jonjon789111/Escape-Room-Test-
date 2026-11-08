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

/* MAIN BACKGROUND */

.stApp {
    background-color: #10131C;
}

/* HEADINGS */

h1 {
    color: #D6B66F;
    text-align: center;
    font-size: 45px;
    font-weight: bold;
}

h2, h3 {
    color: #D6B66F;
}

/* PARAGRAPHS */

p {
    color: #E8EAF0;
    text-align: center;
    font-size: 17px;
}

/* BUTTON DESIGN */

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

/* BUTTON HOVER EFFECT */

.stButton > button:hover {
    background: linear-gradient(135deg, #D6B66F, #F0D99A);
    color: #10131C;
    border: 1px solid #F0D99A;
    transform: translateY(-3px);
    box-shadow: 0px 7px 20px rgba(214, 182, 111, 0.35);
}

/* BUTTON CLICK EFFECT */

.stButton > button:active {
    transform: translateY(1px);
}

</style>
""", unsafe_allow_html=True)

# ==================================
# PAGE NAVIGATION
# ==================================

if "page" not in st.session_state:
    st.session_state.page = "home"

# ==================================
# MAIN MENU SCREEN
# ==================================

elif st.session_state.page == "home":

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

    # PLAY BUTTON

    if st.button("▶ PLAY", use_container_width=True):

        st.session_state.page = "story"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # HOW TO PLAY BUTTON

    if st.button("📖 HOW TO PLAY", use_container_width=True):

        st.session_state.page = "instructions"
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # FOOTER

    st.markdown(
        "<p style='color:#7D879B; font-size:12px;'>"
        "A DIFFERENTIAL CALCULUS ESCAPE GAME"
        "</p>",
        unsafe_allow_html=True
    )


# ==================================
# HOW TO PLAY SCREEN
# ==================================

if st.session_state.page == "instructions":

    st.markdown("<br>", unsafe_allow_html=True)

    st.title("HOW TO PLAY")

    st.markdown(
        "<p>Learn the rules before entering the classroom!</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # OBJECTIVE

    st.subheader("🎯 OBJECTIVE")

    st.write(
        "Escape the locked classroom by completing "
        "all 12 Differential Calculus challenges "
        "across four rooms."
    )

    st.markdown("---")

    # GAME PROGRESSION

    st.subheader("🔑 GAME PROGRESSION")

    st.write("""
    1. Start in Room 1 and solve its three challenges.
    2. Complete all three challenges to earn a key.
    3. Use the key to unlock the next room.
    4. Complete all four rooms to escape.
    """)

    st.markdown("---")

    # LIVES

    st.subheader("❤️ LIVES")

    st.write("""
    - You start with 3 lives.
    - Every incorrect answer costs 1 life.
    - Lose all 3 lives and the game ends.
    """)

    st.markdown("---")

    # TIMER

    st.subheader("⏱️ TIMER")

    st.write("""
    - You have 10 minutes to escape.
    - Every incorrect answer deducts 5 seconds.
    - If the timer reaches zero, the game ends.
    """)

    st.markdown("---")

    # HINTS

    st.subheader("💡 HINTS")

    st.write("""
    - You have 2 hints for the entire game.
    - Each hint reveals one step toward the solution.
    - Hints will not reveal the final answer.
    """)

    st.markdown("---")

    # IMPORTANT RULES

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

    st.markdown("<br>", unsafe_allow_html=True)

    # BACK BUTTON

    if st.button("⬅ BACK TO MAIN MENU", use_container_width=True):

        st.session_state.page = "home"
        st.rerun()
