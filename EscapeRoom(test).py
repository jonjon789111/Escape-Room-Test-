
import streamlit as st
import time
import base64

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="The Locked Classroom",
    page_icon="🔒",
    layout="wide"
)

defaults = {
    "page": "home",
    "lives": 3,
    "hints": 2,
    "time_limit": 600,
    "start_time": None,
    "question_number": 0,

    # ROOM PROGRESS
    "room1_cleared": False,
    "room2_cleared": False,
    "room3_cleared": False,
    "room4_cleared": False,

    # GAME STATUS
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
    blur = ""

    if st.session_state.page != "home":
        blur = "blur(6px)"

   
    with open("klasrum.jpg", "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()


    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;800&family=Cormorant+Garamond:wght@400;500;600&display=swap');

    .stApp {{
        background:
            linear-gradient(
                rgba(16, 24, 39, 0.65),
                rgba(16, 24, 39, 0.65)
            ),
            url("data:image/jpeg;base64,{encoded_image}");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #F4F1EA;
    }}

    .block-container {{
        max-width: 1150px;
        padding-top: 3.5rem !important;
        padding-bottom: 3rem !important;
    }}

    .main-title {{
        font-family: Cinzel, serif;
        font-size: clamp(40px, 5vw, 68px);
        font-weight: 800;
        letter-spacing: 5px;
        color: #F4F1EA;
        text-align: center;
    }}

    .subtitle {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 24px;
        color: #C6B78E;
        text-align: center;
    }}

    .gold-line {{
        width: 75%;
        height: 1px;
        margin: 25px auto;
        background: linear-gradient(to right, transparent, #B59A60, transparent);
    }}

    .section-title {{
        font-family: Cinzel, serif;
        color: #D8B96F;
        font-size: 18px;
        letter-spacing: 3px;
    }}

    .story-text {{
        font-family: 'Cormorant Garamond', serif;
        color: #E0E3E8;
        font-size: 21px;
        line-height: 1.7;
    }}

    div[data-testid="stButton"] button {{
        height: 52px;
        border-radius: 8px;
        font-family: Cinzel, serif;
        font-weight: bold;
        letter-spacing: 2px;
    }}

    div[data-testid="stButton"] button[kind="primary"] {{
        background: #476B56 !important;
        color: white !important;
        border: 1px solid #78947E !important;
    }}

    div[data-testid="stButton"] button[kind="secondary"] {{
        background: #B59A60 !important;
        color: #17202B !important;
        border: 1px solid #D9C28C !important;
    }}

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

    # ROOM PROGRESS
    st.session_state.room1_cleared = False
    st.session_state.room2_cleared = False
    st.session_state.room3_cleared = False
    st.session_state.room4_cleared = False

    # GAME STATUS
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


def game_status():

    # Center the three status indicators
    left, lives, hints, timer, right = st.columns(
        [1, 2, 2, 2, 1]
    )

    with lives:
        st.metric("LIVES", st.session_state.lives)

    with hints:
        st.metric("HINTS", st.session_state.hints)

    with timer:
        live_timer()


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

    header(
        "THE LOCKED CLASSROOM",
        "THE STORY",
        "An escape room adventure"
    )

    st.markdown("### THE FINAL BELL HAS RUNG...")

    st.write(
        "As you prepare to leave, you reach for the door. "
        "But something is wrong. **It's locked.**"
    )

    st.info(
        "Suddenly, strange mathematical challenges begin appearing "
        "around the classroom."
    )

    st.markdown("### FOUR AREAS. FOUR CHALLENGES.")
    st.caption("Click an unlocked room to continue your adventure.")

    col1, col2 = st.columns(2, gap="large")

    # ROOM 1
    with col1:
        with st.container(border=True):
            st.markdown("### 🖍️ The Blackboard")
            st.caption("Room 1 — Limits")

            if st.session_state.room1_cleared:
                st.success("COMPLETED")

            if st.button("ENTER ROOM 1 →", type="primary", use_container_width=True):
                if st.session_state.start_time is None:
                    start_game()
                else:
                    st.session_state.page = "room1"
                st.rerun()

    # ROOM 2
    with col2:
        with st.container(border=True):
            st.markdown("### 🪑 The Teacher's Desk")
            st.caption("Room 2 — Basic Derivatives (Power Rule)")

            if st.session_state.room2_cleared:
                st.success("COMPLETED")
            elif not st.session_state.room1_cleared:
                st.warning("🔒 LOCKED")

            if st.button(
                "ENTER ROOM 2 →",
                disabled=not st.session_state.room1_cleared,
                use_container_width=True
            ):
                st.session_state.page = "room2"
                st.rerun()

    # ROOM 3
    with col1:
        with st.container(border=True):
            st.markdown("### 🗄️ The Storage Cabinet")
            st.caption("Room 3 — Product, Quotient, and Chain Rules")

            if st.session_state.room3_cleared:
                st.success("COMPLETED")
            elif not st.session_state.room2_cleared:
                st.warning("🔒 LOCKED")

            if st.button(
                "ENTER ROOM 3 →",
                disabled=not st.session_state.room2_cleared,
                use_container_width=True
            ):
                st.session_state.page = "room3"
                st.rerun()

    # ROOM 4
    with col2:
        with st.container(border=True):
            st.markdown("### 🚪 The Exit Door")
            st.caption("Room 4 — Trigonometric Derivatives")

            if st.session_state.room4_cleared:
                st.success("COMPLETED")
            elif not st.session_state.room3_cleared:
                st.warning("🔒 LOCKED")

            if st.button(
                "ENTER ROOM 4 →",
                disabled=not st.session_state.room3_cleared,
                use_container_width=True
            ):
                st.session_state.page = "room4"
                st.rerun()

    st.write("")

    st.warning(
        "Complete each room to unlock the next one "
        "and collect all four keys."
    )

    st.markdown("### BUT REMEMBER...")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("LIVES", st.session_state.lives)
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

    if st.button("← BACK TO MENU", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()



# ==========================================
# INSTRUCTIONS PAGE
# ==========================================

def instructions_page():

    design()

    header(
        "THE LOCKED CLASSROOM",
        "HOW TO PLAY",
        "Read carefully before entering."
    )

    left, center, right = st.columns([1, 5, 1])

    with center:
        with st.container(border=True):
            st.markdown(
                '<div class="section-title">YOUR OBJECTIVE</div>',
                unsafe_allow_html=True
            )

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
        '<div class="section-title" style="text-align:center">'
        'YOUR FOUR DESTINATIONS</div>',
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

    left, back, gap, start, right = st.columns(
        [1.5, 2.5, 0.3, 2.5, 1.5]
    )

    with back:
        if st.button("BACK TO MENU", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    with start:
        if st.button(
            "START GAME →",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page="story"
            st.rerun()

# ==========================================
# ROOM 1 — THE BLACKBOARD
# ==========================================

def room1():

    design()

    header(
        "ROOM 01",
        "THE BLACKBOARD",
        "The first challenge — Limits"
    )

    if st.session_state.game_over:

        st.error("GAME OVER! You ran out of lives or time.")

        if st.button("RETURN TO MENU"):
            st.session_state.page = "home"
            st.rerun()

        return

    game_status()

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    # CHALLENGE 1
    if st.session_state.question_number == 0:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">CHALLENGE 1 OF 3</div>',
                unsafe_allow_html=True
            )

            st.write("Find the limit:")
            st.latex(r"\lim_{x\to2}(3x+4)")

            answer = st.text_input("YOUR ANSWER", key="answer1")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if answer.strip() == "10":
                        st.session_state.feedback = "correct"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"

                    st.rerun()

            with right:
                if st.button("USE HINT", type="secondary", use_container_width=True):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint("Substitute x = 2 into the expression.")

                    st.rerun()

    # CHALLENGE 2
    elif st.session_state.question_number == 1:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">CHALLENGE 2 OF 3</div>',
                unsafe_allow_html=True
            )

            st.write("Evaluate the following limit:")
            st.latex(r"\lim_{x\to2}\frac{x^2-4}{x-2}")

            answer = st.text_input("YOUR ANSWER", key="answer2")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if answer.strip() == "4":
                        st.session_state.feedback = "correct"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"

                    st.rerun()

            with right:
                if st.button("USE HINT", type="secondary", use_container_width=True):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint("Factor the numerator into (x - 2)(x + 2).")

                    st.rerun()

    # CHALLENGE 3
    elif st.session_state.question_number == 2:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">CHALLENGE 3 OF 3</div>',
                unsafe_allow_html=True
            )

            st.write("Find the limit:")
            st.latex(r"\lim_{x\to1}\frac{x^2+3x-4}{x-1}")

            answer = st.text_input("YOUR ANSWER", key="answer3")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if answer.strip() == "5":
                        st.session_state.feedback = "correct"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"

                    st.rerun()

            with right:
                if st.button("USE HINT", type="secondary", use_container_width=True):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint("Factor the numerator into (x - 1)(x + 4).")

                    st.rerun()

    # FEEDBACK
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
                st.session_state.page = "story"

            st.rerun()

    elif st.session_state.feedback == "wrong":

        st.error("Incorrect! One life and five seconds deducted.")

        st.session_state.feedback = ""

        if st.session_state.game_over:
            st.rerun()

    # HINT MESSAGE
    if st.session_state.hint_message:
        st.info(st.session_state.hint_message)

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)


# ==========================================
# ROOM 2 — THE TEACHER'S DESK
# ==========================================

def room2():

    design()

    header(
        "ROOM 02",
        "THE TEACHER'S DESK",
        "The second challenge — Basic Derivatives"
    )

    if st.session_state.game_over:

        st.error("GAME OVER! You ran out of lives or time.")

        if st.button("RETURN TO MENU"):
            st.session_state.page = "home"
            st.rerun()

        return

    game_status()

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    # CHALLENGE 1 (Drawer 1 - Power Rule)
    if st.session_state.question_number == 0:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">DRAWER 1 OF 3 — POWER RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = 4x^3")

            answer = st.text_input("YOUR ANSWER (e.g. 2x^2)", key="r2_answer1")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if answer.replace(" ", "").lower() == "12x^2":
                        st.session_state.feedback = "correct"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"

                    st.rerun()

            with right:
                if st.button("USE HINT", type="secondary", use_container_width=True):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint("Apply the Power Rule: bring down the exponent 3, multiply by 4, and subtract 1 from the exponent.")

                    st.rerun()

    # CHALLENGE 2 (Drawer 2 - Constant, Sum, and Difference Rules)
    elif st.session_state.question_number == 1:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">DRAWER 2 OF 3 — SUM & DIFFERENCE RULES</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = 5x^2 - 3x + 7")

            answer = st.text_input("YOUR ANSWER", key="r2_answer2")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if answer.replace(" ", "").lower() == "10x-3":
                        st.session_state.feedback = "correct"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"

                    st.rerun()

            with right:
                if st.button("USE HINT", type="secondary", use_container_width=True):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint("Differentiate each term separately. Remember that the derivative of a constant (7) is 0.")

                    st.rerun()

    # CHALLENGE 3 (Drawer 3 - Combination of Basic Rules)
    elif st.session_state.question_number == 2:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">DRAWER 3 OF 3 — COMBINATION OF BASIC RULES</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = 10x^4 + 9x^3 + 4x^2 + x + 67")

            answer = st.text_input("YOUR ANSWER", key="r2_answer3")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if answer.replace(" ", "").lower() == "40x^3+27x^2+8x+1":
                        st.session_state.feedback = "correct"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"

                    st.rerun()

            with right:
                if st.button("USE HINT", type="secondary", use_container_width=True):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint("Apply the Power Rule to each term: the derivative of x is 1, and the derivative of 67 is 0.")

                    st.rerun()

    # FEEDBACK
    if st.session_state.feedback == "correct":

        st.success("Correct! You solved the challenge.")

        if st.button("CONTINUE", type="primary"):

            st.session_state.question_number += 1
            st.session_state.feedback = ""
            st.session_state.hint_message = ""
            st.session_state.hint_used_this_question = False

            if st.session_state.question_number == 3:

                st.session_state.room2_cleared = True
                st.session_state.question_number = 0
                st.session_state.page = "story"

            st.rerun()

    elif st.session_state.feedback == "wrong":

        st.error("Incorrect! One life and five seconds deducted.")

        st.session_state.feedback = ""

        if st.session_state.game_over:
            st.rerun()

    # HINT MESSAGE
    if st.session_state.hint_message:
        st.info(st.session_state.hint_message)

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

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
