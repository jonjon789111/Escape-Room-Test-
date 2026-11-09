
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

   # ==========================================
    # HOMEPAGE DESIGN
    # ==========================================

    st.markdown("""
        <style>

        /* BACKGROUND */
        .stApp {
            background-color: #101827;
        }

        /* MAIN CONTENT WIDTH */
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* TITLE */
        .home-title {
            font-family: 'Cinzel', serif;
            font-size: clamp(42px, 5vw, 68px);
            font-weight: 800;
            letter-spacing: 5px;
            color: #F4F1EA;
            text-align: center;
            text-shadow: 0 0 25px rgba(180, 190, 210, 0.2);
            margin-bottom: 8px;
        }

        /* SUBTITLE */
        .home-subtitle {
            font-family: 'Cormorant Garamond', serif;
            font-size: 27px;
            color: #C6B78E;
            text-align: center;
            letter-spacing: 3px;
            margin-bottom: 5px;
        }

        /* TAGLINE */
        .home-tagline {
            font-family: 'Cormorant Garamond', serif;
            font-size: 19px;
            color: #AAB2C0;
            text-align: center;
            letter-spacing: 2px;
        }

        /* DIVIDER */
        .gold-divider {
            width: 75%;
            height: 1px;
            background: linear-gradient(
                to right,
                transparent,
                #B59A60,
                transparent
            );
            margin: 35px auto;
        }

        /* OBJECTIVE TITLE */
        .objective-heading {
            color: #C6B78E;
            font-family: 'Cinzel', serif;
            font-size: 23px;
            font-weight: bold;
            letter-spacing: 4px;
            text-align: center;
        }

        /* OBJECTIVE CONTAINER */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid #766747;
            background-color: rgba(31, 42, 59, 0.85);
            border-radius: 12px;
        }

        /* BUTTON BASE */
        div.stButton > button {
            height: 60px;
            width: 100%;
            border-radius: 8px;
            font-family: 'Cinzel', serif;
            font-size: 17px;
            font-weight: 700;
            letter-spacing: 3px;
            transition: 0.2s ease;
        }

        /* PLAY BUTTON */
        .play-button div.stButton > button {
            background-color: #476B56 !important;
            color: #FFFFFF !important;
            border: 1px solid #78947E !important;
        }

        .play-button div.stButton > button:hover {
            background-color: #5B8469 !important;
            border-color: #B5C9AD !important;
            color: #FFFFFF !important;
        }

        /* HOW TO PLAY BUTTON */
        .instructions-button div.stButton > button {
            background-color: #B59A60 !important;
            color: #17202B !important;
            border: 1px solid #D9C28C !important;
        }

        .instructions-button div.stButton > button:hover {
            background-color: #D0B77C !important;
            border-color: #F0DFB2 !important;
            color: #17202B !important;
        }

        /* FOOTER */
        .home-footer {
            color: #7F8999;
            font-family: 'Cormorant Garamond', serif;
            font-size: 16px;
            text-align: center;
            letter-spacing: 2px;
            margin-top: 45px;
        }

        </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # TITLE
    # ==========================================

    st.markdown("""
        <div class="home-title">
            THE LOCKED CLASSROOM
        </div>

        <div class="home-subtitle">
            A Differential Calculus Escape Game
        </div>

        <div class="home-tagline">
            FOUR ROOMS. TWELVE CHALLENGES. ONE WAY OUT.
        </div>

        <div class="gold-divider"></div>
    """, unsafe_allow_html=True)


    # ==========================================
    # OBJECTIVE
    # ==========================================

    left, center, right = st.columns([1, 5, 1])

    with center:

        with st.container(border=True):

            st.markdown(
                '<div class="objective-heading">OBJECTIVE</div>',
                unsafe_allow_html=True
            )

            st.write("")

            st.markdown(
                """
                <div style="
                    text-align: center;
                    color: #E0E3E8;
                    font-size: 19px;
                    line-height: 1.7;
                ">
                    Solve Differential Calculus challenges to escape
                    the locked classroom.<br>
                    Can you complete all four rooms before time runs out?
                </div>
                """,
                unsafe_allow_html=True
            )


    # ==========================================
    # BUTTONS
    # ==========================================

    st.write("")
    st.write("")

    left, play_col, gap, instructions_col, right = st.columns(
        [1.5, 2.5, 0.3, 2.5, 1.5]
    )

    with play_col:

        st.markdown('<div class="play-button">', unsafe_allow_html=True)

        if st.button("PLAY", use_container_width=True):

            st.session_state.page = "story"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


    with instructions_col:

        st.markdown(
            '<div class="instructions-button">',
            unsafe_allow_html=True
        )

        if st.button("HOW TO PLAY", use_container_width=True):

            st.session_state.page = "instructions"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # FOOTER
    # ==========================================

    st.markdown("""
        <div class="home-footer">
            THINK CAREFULLY. SOLVE WISELY. ESCAPE.
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# STORY PAGE
# ==========================================

def story_page():

    # ==========================================
    # STORY PAGE DESIGN
    # ==========================================

    st.markdown("""
        <style>

        .stApp {
            background-color: #101827;
        }

        .block-container {
            max-width: 1150px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .story-label {
            color: #B59A60;
            font-family: 'Cinzel', serif;
            font-size: 15px;
            letter-spacing: 5px;
            text-align: center;
        }

        .story-title {
            color: #F4F1EA;
            font-family: 'Cinzel', serif;
            font-size: clamp(38px, 5vw, 60px);
            font-weight: 800;
            letter-spacing: 5px;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(180,190,210,0.2);
        }

        .story-subtitle {
            color: #C6B78E;
            font-family: 'Cormorant Garamond', serif;
            font-size: 23px;
            letter-spacing: 2px;
            text-align: center;
        }

        .story-divider {
            width: 75%;
            height: 1px;
            background: linear-gradient(
                to right,
                transparent,
                #B59A60,
                transparent
            );
            margin: 30px auto;
        }

        .story-section-title {
            color: #C6B78E;
            font-family: 'Cinzel', serif;
            font-size: 21px;
            letter-spacing: 3px;
            font-weight: bold;
        }

        .story-paragraph {
            color: #E0E3E8;
            font-family: 'Cormorant Garamond', serif;
            font-size: 21px;
            line-height: 1.8;
        }

        .story-warning {
            color: #D8B96F;
            font-family: 'Cinzel', serif;
            font-size: 17px;
            letter-spacing: 2px;
            text-align: center;
            font-weight: bold;
        }

        .story-footer {
            color: #7F8999;
            font-family: 'Cormorant Garamond', serif;
            font-size: 16px;
            text-align: center;
            letter-spacing: 2px;
            margin-top: 35px;
        }

        div[data-testid="stButton"] button {
            height: 55px;
            border-radius: 8px;
            font-family: 'Cinzel', serif;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 2px;
        }

        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #476B56 !important;
            color: white !important;
            border: 1px solid #78947E !important;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #5B8469 !important;
            color: white !important;
        }

        div[data-testid="stButton"] button[kind="secondary"] {
            background-color: #B59A60 !important;
            color: #17202B !important;
            border: 1px solid #D9C28C !important;
        }

        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background-color: #D0B77C !important;
            color: #17202B !important;
        }

        </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # STORY HEADER
    # ==========================================

    st.markdown("""
        <div class="story-label">THE LOCKED CLASSROOM</div>

        <div class="story-title">
            THE STORY
        </div>

        <div class="story-subtitle">
            Every classroom holds a secret.
        </div>

        <div class="story-divider"></div>
    """, unsafe_allow_html=True)


    # ==========================================
    # STORY CONTENT
    # ==========================================

    left, center, right = st.columns([1, 5, 1])

    with center:

        with st.container(border=True):

            st.markdown(
                '<div class="story-section-title">11:47 PM — THE CLASSROOM</div>',
                unsafe_allow_html=True
            )

            st.write("")

            st.markdown("""
                <div class="story-paragraph">
                    It is already late, and you are the last student
                    inside the classroom.
                    <br><br>
                    As you prepare to leave, you reach for the door.
                    But something is wrong. It is locked.
                    <br><br>
                    Suddenly, strange mathematical challenges begin
                    appearing around the classroom. The blackboard,
                    teacher's desk, storage cabinet, and exit door
                    each hold a series of Differential Calculus problems.
                    <br><br>
                    A message appears on the board:
                </div>
            """, unsafe_allow_html=True)

            st.write("")

            st.markdown("""
                <div style="
                    text-align: center;
                    color: #D8B96F;
                    font-family: 'Cinzel', serif;
                    font-size: 23px;
                    font-weight: bold;
                    letter-spacing: 2px;
                    padding: 20px;
                    border-top: 1px solid #766747;
                    border-bottom: 1px solid #766747;
                ">
                    SOLVE THE CHALLENGES.<br>
                    COLLECT THE KEYS.<br>
                    FIND YOUR WAY OUT.
                </div>
            """, unsafe_allow_html=True)

            st.write("")

            st.markdown("""
                <div class="story-paragraph">
                    You must explore all four areas and complete
                    three challenges in each room to unlock the next.
                    Every correct answer brings you closer to freedom.
                    <br><br>
                    But be careful. Every wrong answer costs you
                    one life and five seconds.
                </div>
            """, unsafe_allow_html=True)


    # ==========================================
    # GAME WARNING
    # ==========================================

    st.write("")
    st.markdown("""
        <div class="story-warning">
            YOU HAVE 10 MINUTES. THREE LIVES. TWO HINTS.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="story-divider"></div>
    """, unsafe_allow_html=True)


    # ==========================================
    # NAVIGATION BUTTONS
    # ==========================================

    left, back_col, gap, start_col, right = st.columns(
        [1.5, 2.5, 0.3, 2.5, 1.5]
    )

    with back_col:

        if st.button(
            "BACK TO MENU",
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.page = "home"
            st.rerun()

    with start_col:

        if st.button(
            "START GAME",
            use_container_width=True,
            type="primary"
        ):
            start_game()
            st.rerun()


    # ==========================================
    # FOOTER
    # ==========================================

    st.markdown("""
        <div class="story-footer">
            YOUR ESCAPE BEGINS NOW.
        </div>
    """, unsafe_allow_html=True)



# ==========================================
# INSTRUCTIONS PAGE
# ==========================================

def instructions_page():

     # ==========================================
    # HOW TO PLAY DESIGN
    # ==========================================

    st.markdown("""
        <style>

        .stApp {
            background-color: #101827;
        }

        .block-container {
            max-width: 1150px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .instruction-label {
            color: #B59A60;
            font-family: 'Cinzel', serif;
            font-size: 15px;
            letter-spacing: 5px;
            text-align: center;
        }

        .instruction-title {
            color: #F4F1EA;
            font-family: 'Cinzel', serif;
            font-size: clamp(38px, 5vw, 60px);
            font-weight: 800;
            letter-spacing: 5px;
            text-align: center;
            margin-top: 10px;
            text-shadow: 0 0 20px rgba(180,190,210,0.2);
        }

        .instruction-subtitle {
            color: #C6B78E;
            font-family: 'Cormorant Garamond', serif;
            font-size: 23px;
            letter-spacing: 2px;
            text-align: center;
        }

        .instruction-divider {
            width: 75%;
            height: 1px;
            background: linear-gradient(
                to right,
                transparent,
                #B59A60,
                transparent
            );
            margin: 30px auto;
        }

        .section-heading {
            color: #C6B78E;
            font-family: 'Cinzel', serif;
            font-size: 19px;
            font-weight: bold;
            letter-spacing: 2px;
        }

        .instruction-text {
            color: #E0E3E8;
            font-family: 'Cormorant Garamond', serif;
            font-size: 19px;
            line-height: 1.7;
        }

        .instruction-number {
            color: #D8B96F;
            font-family: 'Cinzel', serif;
            font-size: 25px;
            font-weight: bold;
        }

        .instruction-footer {
            color: #7F8999;
            font-family: 'Cormorant Garamond', serif;
            font-size: 16px;
            text-align: center;
            letter-spacing: 2px;
            margin-top: 35px;
        }

        div[data-testid="stButton"] button {
            height: 55px;
            border-radius: 8px;
            font-family: 'Cinzel', serif;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 2px;
        }

        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #476B56 !important;
            color: white !important;
            border: 1px solid #78947E !important;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #5B8469 !important;
            color: white !important;
        }

        div[data-testid="stButton"] button[kind="secondary"] {
            background-color: #B59A60 !important;
            color: #17202B !important;
            border: 1px solid #D9C28C !important;
        }

        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background-color: #D0B77C !important;
            color: #17202B !important;
        }

        </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # HEADER
    # ==========================================

    st.markdown("""
        <div class="instruction-label">THE LOCKED CLASSROOM</div>

        <div class="instruction-title">
            HOW TO PLAY
        </div>

        <div class="instruction-subtitle">
            Read carefully before entering.
        </div>

        <div class="instruction-divider"></div>
    """, unsafe_allow_html=True)


    # ==========================================
    # GAME OBJECTIVE
    # ==========================================

    left, center, right = st.columns([1, 5, 1])

    with center:

        with st.container(border=True):

            st.markdown(
                '<div class="section-heading">YOUR OBJECTIVE</div>',
                unsafe_allow_html=True
            )

            st.markdown("""
                <div class="instruction-text">
                    Complete all four rooms by answering three
                    Differential Calculus questions in each room.
                    Solve every challenge to collect the keys and
                    unlock your way out.
                </div>
            """, unsafe_allow_html=True)


    st.write("")


    # ==========================================
    # GAME RULES
    # ==========================================

    st.markdown("""
        <div class="instruction-divider"></div>
        <div class="section-heading" style="text-align:center;">
            GAME RULES
        </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("""
                <div class="instruction-number">01</div>
                <div class="section-heading">FOUR ROOMS</div>
                <div class="instruction-text">
                    Complete three questions in each room.
                    Clear a room to unlock the next one.
                </div>
                <br>

                <div class="instruction-number">02</div>
                <div class="section-heading">THREE LIVES</div>
                <div class="instruction-text">
                    You start with three lives.
                    Every incorrect answer costs one life.
                </div>
                <br>

                <div class="instruction-number">03</div>
                <div class="section-heading">TIME LIMIT</div>
                <div class="instruction-text">
                    You have ten minutes to complete all
                    twelve challenges.
                </div>
            """, unsafe_allow_html=True)

    with col2:

        with st.container(border=True):

            st.markdown("""
                <div class="instruction-number">04</div>
                <div class="section-heading">TWO HINTS</div>
                <div class="instruction-text">
                    You have two hints for the entire game.
                    Each question can only use one hint.
                </div>
                <br>

                <div class="instruction-number">05</div>
                <div class="section-heading">TIME PENALTY</div>
                <div class="instruction-text">
                    Every incorrect answer also deducts
                    five seconds from your remaining time.
                </div>
                <br>

                <div class="instruction-number">06</div>
                <div class="section-heading">GAME OVER</div>
                <div class="instruction-text">
                    The game ends when you run out of lives
                    or when the timer reaches zero.
                </div>
            """, unsafe_allow_html=True)


    # ==========================================
    # ROOM GUIDE
    # ==========================================

    st.markdown("""
        <div class="instruction-divider"></div>
        <div class="section-heading" style="text-align:center;">
            YOUR FOUR DESTINATIONS
        </div>
    """, unsafe_allow_html=True)

    st.write("")

    room_col1, room_col2, room_col3, room_col4 = st.columns(4)

    rooms = [
        ("ROOM 01", "BLACKBOARD", "Limits"),
        ("ROOM 02", "TEACHER'S DESK", "Basic Derivatives"),
        ("ROOM 03", "STORAGE CABINET", "Product, Quotient, and Chain Rules"),
        ("ROOM 04", "EXIT DOOR", "Trigonometric Derivatives")
    ]

    for column, room in zip(
        [room_col1, room_col2, room_col3, room_col4],
        rooms
    ):

        with column:

            with st.container(border=True):

                st.markdown(
                    f"""
                    <div style="
                        color:#D8B96F;
                        font-family:'Cinzel',serif;
                        font-size:13px;
                        letter-spacing:2px;
                        text-align:center;
                    ">
                        {room[0]}
                    </div>

                    <div style="
                        color:#C6B78E;
                        font-family:'Cinzel',serif;
                        font-size:15px;
                        font-weight:bold;
                        text-align:center;
                        margin-top:12px;
                    ">
                        {room[1]}
                    </div>

                    <div style="
                        color:#E0E3E8;
                        font-family:'Cormorant Garamond',serif;
                        font-size:17px;
                        text-align:center;
                        margin-top:10px;
                    ">
                        {room[2]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ==========================================
    # NAVIGATION BUTTONS
    # ==========================================

    st.markdown('<div class="instruction-divider"></div>',
                unsafe_allow_html=True)

    left, back_col, gap, start_col, right = st.columns(
        [1.5, 2.5, 0.3, 2.5, 1.5]
    )

    with back_col:

        if st.button(
            "BACK TO MENU",
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.page = "home"
            st.rerun()

    with start_col:

        if st.button(
            "START GAME",
            use_container_width=True,
            type="primary"
        ):
            start_game()
            st.rerun()


    # ==========================================
    # FOOTER
    # ==========================================

    st.markdown("""
        <div class="instruction-footer">
            KNOW THE RULES. TRUST YOUR SOLUTIONS. ESCAPE.
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# ROOM 1: THE BLACKBOARD
# ==========================================

def room1():

     st.markdown("""
        <style>
        .stApp {
            background-color: #101827;
        }

        .block-container {
            max-width: 1150px;
            padding-top: 2rem;
        }

        .room-label {
            color: #B59A60;
            font-family: 'Cinzel', serif;
            font-size: 14px;
            letter-spacing: 5px;
            text-align: center;
        }

        .room-title {
            color: #F4F1EA;
            font-family: 'Cinzel', serif;
            font-size: 48px;
            font-weight: bold;
            letter-spacing: 4px;
            text-align: center;
        }

        .room-subtitle {
            color: #C6B78E;
            font-family: 'Cormorant Garamond', serif;
            font-size: 23px;
            text-align: center;
        }

        .room-divider {
            width: 75%;
            height: 1px;
            background: linear-gradient(
                to right, transparent, #B59A60, transparent
            );
            margin: 25px auto;
        }

        .question-label {
            color: #D8B96F;
            font-family: 'Cinzel', serif;
            font-size: 16px;
            letter-spacing: 3px;
        }

        .question-text {
            color: #F4F1EA;
            font-family: 'Cormorant Garamond', serif;
            font-size: 27px;
            line-height: 1.6;
        }

        .room-footer {
            color: #7F8999;
            font-family: 'Cormorant Garamond', serif;
            font-size: 16px;
            text-align: center;
            letter-spacing: 2px;
        }

        div[data-testid="stButton"] button {
            height: 50px;
            border-radius: 8px;
            font-family: 'Cinzel', serif;
            font-weight: bold;
            letter-spacing: 2px;
        }

        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #476B56 !important;
            color: white !important;
            border: 1px solid #78947E !important;
        }

        div[data-testid="stButton"] button[kind="secondary"] {
            background-color: #B59A60 !important;
            color: #17202B !important;
            border: 1px solid #D9C28C !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # HEADER

    st.markdown("""    
        <div class="room-label">ROOM 01</div>
        <div class="room-title">THE BLACKBOARD</div>
        <div class="room-subtitle">The first challenge — Limits</div>
        <div class="room-divider"></div>
    """, unsafe_allow_html=True)

    # GAME STATUS

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("LIVES", st.session_state.lives)

    with col2:
        st.metric("HINTS", st.session_state.hints)

    with col3:
        live_timer()

    st.markdown('<div class="room-divider"></div>',
                unsafe_allow_html=True)

    # QUESTIONS

    questions = [
        {
            "question": "Find the limit:",
            "formula": r"\lim_{x \to 2}(3x+4)",
            "answer": "10",
            "hint": "Substitute x = 2 into the expression."
        },
        {
            "question": "Evaluate the following limit:",
            "formula": r"\lim_{x \to 2}\frac{x^2-4}{x-2}",
            "answer": "4",
            "hint": "Factor the numerator into (x - 2)(x + 2)."
        },
        {
            "question": "Find the limit:",
            "formula": r"\lim_{x \to 1}\frac{x^2+3x-4}{x-1}",
            "answer": "5",
            "hint": "Factor the numerator into (x - 1)(x + 4)."
        }
    ]

    q = questions[st.session_state.question_number]

    left, center, right = st.columns([1, 5, 1])

    with center:

        with st.container(border=True):

            st.markdown(
                f'<div class="question-label">CHALLENGE '
                f'{st.session_state.question_number + 1} OF 3</div>',
                unsafe_allow_html=True
            )

            st.write("")

            st.markdown(
                f'<div class="question-text">{q["question"]}</div>',
                unsafe_allow_html=True
            )

            st.latex(q["formula"])

            st.write("")

            answer = st.text_input(
                "YOUR ANSWER",
                key=f"room1_answer_{st.session_state.question_number}"
            )

            if st.button(
                "SUBMIT ANSWER",
                use_container_width=True,
                type="primary"
            ):

                if answer.strip() == q["answer"]:
                    st.session_state.feedback = "correct"
                else:
                    wrong_answer()
                    st.session_state.feedback = "wrong"

                st.rerun()

            if st.button(
                "USE HINT",
                use_container_width=True,
                type="secondary"
            ):
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

                    if st.session_state.question_number >= 3:
                        st.session_state.room1_cleared = True
                        st.session_state.page = "room2"

                    st.rerun()

            elif st.session_state.feedback == "wrong":
                st.error("Incorrect answer! You lost one life and five seconds.")
                st.session_state.feedback = ""

    st.markdown('<div class="room-divider"></div>',
                unsafe_allow_html=True)

    st.markdown("""
        <div class="room-footer">
            THINK BEFORE YOU ANSWER.
        </div>
    """, unsafe_allow_html=True)



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
