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

    # KEY COLLECTION
    "keys_collected": [],

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

    blur = "blur(6px)" if st.session_state.page != "home" else "none"

    with open("klasrum.jpg", "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()

    st.markdown(f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;800&family=Cormorant+Garamond:wght@400;500;600&display=swap');

    /* BACKGROUND */

    .stApp {{
        background: transparent;
        color: #F4F1EA;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: -10px;
        z-index: -1;
        background-image:
            linear-gradient(
                rgba(16, 24, 39, 0.65),
                rgba(16, 24, 39, 0.65)
            ),
            url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        filter: {blur};
    }}

    /* PAGE SPACING */

    .block-container {{
        max-width: 1150px;
        padding-top: 3.5rem !important;
        padding-bottom: 3rem !important;
    }}

    /* MAIN TITLE */

    .main-title {{
        font-family: Cinzel, serif;
        font-size: clamp(40px, 5vw, 68px);
        font-weight: 800;
        letter-spacing: 5px;
        color: #F4F1EA;
        text-align: center;
    }}

    /* SUBTITLE */

    .subtitle {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 24px;
        color: #C6B78E;
        text-align: center;
    }}

    /* GOLD DIVIDER */

    .gold-line {{
        width: 75%;
        height: 1px;
        margin: 25px auto;
        background: linear-gradient(
            to right,
            transparent,
            #B59A60,
            transparent
        );
    }}

    /* SECTION TITLE */

    .section-title {{
        font-family: Cinzel, serif;
        color: #D8B96F;
        font-size: 18px;
        letter-spacing: 3px;
    }}

    /* STORY TEXT */

    .story-text {{
        font-family: 'Cormorant Garamond', serif;
        color: #E0E3E8;
        font-size: 21px;
        line-height: 1.7;
    }}

    /* BUTTONS */

    div[data-testid="stButton"] button {{
        height: 52px;
        border-radius: 8px;
        font-family: Cinzel, serif;
        font-weight: bold;
        letter-spacing: 2px;
    }}

    /* PLAY BUTTON */

    div[data-testid="stButton"] button[kind="primary"] {{
        background: #476B56 !important;
        color: white !important;
        border: 1px solid #78947E !important;
    }}

    /* SECONDARY BUTTONS */

    div[data-testid="stButton"] button[kind="secondary"] {{
        background: #B59A60 !important;
        color: #17202B !important;
        border: 1px solid #D9C28C !important;
    }}

    /* GAME HUD */

    .hud-container {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px auto;
        max-width: 750px;
    }}

    .hud-item {{
        flex: 1;
        background: rgba(23, 34, 51, 0.90);
        border: 1px solid #8C774D;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }}

    .hud-icon {{
        font-size: 25px;
        color: #D8B96F;
    }}

    .hud-label {{
        font-family: Cinzel, serif;
        font-size: 12px;
        color: #C6B78E;
        letter-spacing: 2px;
    }}

    .hud-value {{
        font-family: Cinzel, serif;
        font-size: 27px;
        font-weight: bold;
        color: #F4F1EA;
    }}

    </style>
    """, unsafe_allow_html=True)

def floating_notification():

    notification = st.session_state.get("notification", "")

    if not notification:
        return

    notification_type = st.session_state.get(
        "notification_type", "success"
    )

    colors = {
        "success": "#3cb878",
        "error": "#d9534f",
        "warning": "#d9a441",
        "info": "#4b91c9"
    }

    color = colors.get(notification_type, "#d9a441")

    # UNIQUE ID FOR EVERY RENDER
    unique_id = time.time_ns()

    st.markdown(f"""
        <style>

        .floating-notification-{unique_id} {{
            position: fixed;
            top: 25px;
            right: 25px;
            z-index: 999999;
            background: rgba(20, 20, 20, 0.96);
            border-left: 5px solid {color};
            color: white;
            padding: 16px 25px;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.5);
            font-size: 16px;

            animation:
                notifSlide{unique_id} 0.5s ease,
                notifFade{unique_id} 0.5s ease 2.5s forwards;

            pointer-events: none;
        }}

        @keyframes notifSlide{unique_id} {{
            from {{
                opacity: 0;
                transform: translateX(100px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        @keyframes notifFade{unique_id} {{
            to {{
                opacity: 0;
            }}
        }}

        </style>

        <div class="floating-notification-{unique_id}">
            {notification}
        </div>
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
    st.session_state.keys_collected = []

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
def game_status():

    if st.session_state.start_time is None:
        remaining = st.session_state.time_limit
    else:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, int(st.session_state.time_limit - elapsed))

    minutes, seconds = divmod(remaining, 60)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="♥ LIVES",
            value=st.session_state.lives
        )

    with col2:
        st.metric(
            label="✦ HINTS",
            value=st.session_state.hints
        )

    with col3:
        st.metric(
            label="◷ TIME LEFT",
            value=f"{minutes:02d}:{seconds:02d}"
        )

    st.markdown("---")

    if remaining <= 0:
        st.session_state.game_over = True
        st.rerun()

def key_inventory():

    keys = {
        "Bronze Key": "Room 1",
        "Silver Key": "Room 2",
        "Gold Key": "Room 3",
        "Crystal Key": "Room 4"
    }

    collected = len(st.session_state.keys_collected)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: Arial, sans-serif;
        }}

        .key-inventory {{
            background: rgba(12, 18, 30, 0.94);
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 16px;
            padding: 22px;
            color: white;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(10px);
        }}

        .key-title {{
            font-size: 22px;
            font-weight: bold;
            color: #f5d58a;
            margin-bottom: 8px;
        }}

        .key-count {{
            color: #cccccc;
            font-size: 13px;
            margin-bottom: 18px;
        }}

        .key-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 13px;
            margin-top: 9px;
            border-radius: 9px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 14px;
        }}

        .key-collected {{
            color: #8ee6a1;
            font-weight: bold;
        }}

        .key-locked {{
            color: #bbbbbb;
        }}
    </style>
    </head>

    <body>
        <div class="key-inventory">
            <div class="key-title">🔑 KEY INVENTORY</div>

            <div class="key-count">
                {collected}/4 KEYS COLLECTED
            </div>
    """

    for key in keys:
        if key in st.session_state.keys_collected:
            status = "🔓 COLLECTED"
            css_class = "key-collected"
        else:
            status = "🔒 LOCKED"
            css_class = "key-locked"

        html += f"""
            <div class="key-item">
                <span>{key}</span>
                <span class="{css_class}">{status}</span>
            </div>
        """

    html += """
        </div>
    </body>
    </html>
    """

    st.components.v1.html(
    html,
    height=350,
    scrolling=False,
    tab_index=None
)

def progress_bar():

    completed_rooms = sum([
        st.session_state.room1_cleared,
        st.session_state.room2_cleared,
        st.session_state.room3_cleared,
        st.session_state.room4_cleared
    ])

    completed_questions = (completed_rooms * 3) + st.session_state.question_number

    progress = min(completed_questions / 12, 1.0)

    st.markdown("### ✦ ESCAPE PROGRESS")

    st.progress(
        progress,
        text=f"{completed_questions}/12 CHALLENGES COMPLETED"
    )

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
            reset_game()
            st.session_state.page = "home"
            st.rerun()

        return

    game_status()
    progress_bar()
    floating_notification()
    key_inventory()

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
                        st.session_state.notification = "✓ CORRECT ANSWER!"
                        st.session_state.notification_type = "success"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"
                        st.session_state.notification = "✕ INCORRECT ANSWER!"
                        st.session_state.notification_type = "error"

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
                        st.session_state.notification = "✓ CORRECT ANSWER!"
                        st.session_state.notification_type = "success"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"
                        st.session_state.notification = "✕ INCORRECT ANSWER!"
                        st.session_state.notification_type = "error"

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
                        st.session_state.notification = "✓ CORRECT ANSWER!"
                        st.session_state.notification_type = "success"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"
                        st.session_state.notification = "✕ INCORRECT ANSWER!"
                        st.session_state.notification_type = "error"

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
            st.session_state.notification = ""
            st.session_state.notification_type = ""

            st.session_state.question_number += 1
            st.session_state.feedback = ""
            st.session_state.hint_message = ""
            st.session_state.hint_used_this_question = False

            if st.session_state.question_number == 3:

                st.session_state.room1_cleared = True

                # COLLECT BRONZE KEY
                if "Bronze Key" not in st.session_state.keys_collected:
                    st.session_state.keys_collected.append("Bronze Key")

                st.session_state.notification = "🔑 BRONZE KEY COLLECTED!"
                st.session_state.notification_type = "warning"

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
            reset_game()
            st.session_state.page = "home"
            st.rerun()

        return

    game_status()
    progress_bar()
    floating_notification()
    key_inventory()

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
                        st.session_state.notification = "✓ CORRECT ANSWER!"
                        st.session_state.notification_type = "success"

                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"
                        st.session_state.notification = "✕ INCORRECT ANSWER!"
                        st.session_state.notification_type = "error"

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
                        st.session_state.notification = "✓ CORRECT ANSWER!"
                        st.session_state.notification_type = "success"

                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"
                        st.session_state.notification = "✕ INCORRECT ANSWER!"
                        st.session_state.notification_type = "error"

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
                        st.session_state.notification = "✓ CORRECT ANSWER!"
                        st.session_state.notification_type = "success"

                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"
                        st.session_state.notification = "✕ INCORRECT ANSWER!"
                        st.session_state.notification_type = "error"

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
            st.session_state.notification = ""
            st.session_state.notification_type = ""

            st.session_state.question_number += 1
            st.session_state.feedback = ""
            st.session_state.hint_message = ""
            st.session_state.hint_used_this_question = False

            if st.session_state.question_number == 3:

                st.session_state.room2_cleared = True

                # COLLECT SILVER KEY
                if "Silver Key" not in st.session_state.keys_collected:
                    st.session_state.keys_collected.append("Silver Key")

                st.session_state.notification = "🔑 SILVER KEY COLLECTED!"
                st.session_state.notification_type = "warning"

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

def clean_answer(text):
    # Normalizes input so "8 * (2x + 3)^3" and "8(2x+3)^3" are treated the same
    return text.replace(" ", "").replace("*", "").replace("**", "^").lower()


def room3():

    design()

    header(
        "ROOM 03",
        "THE LIBRARY",
        "The third challenge — Product, Quotient & Chain Rules"
    )

    if st.session_state.game_over:

        st.error("GAME OVER! You ran out of lives or time.")

        if st.button("RETURN TO MENU"):
            st.session_state.page = "home"
            st.rerun()

        return

    game_status()
    progress_bar()
    floating_notification()
    key_inventory()

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    # CHALLENGE 1 (Shelf 1 - Product Rule)
    if st.session_state.question_number == 0:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">SHELF 1 OF 3 — PRODUCT RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = x^2(3x + 1)")

            answer = st.text_input("YOUR ANSWER (e.g. 2x^2+3x)", key="r3_answer1")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if clean_answer(answer) in ["9x^2+2x", "2x+9x^2"]:
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
                        use_hint("Product Rule: (uv)' = u'v + uv'. Let u = x^2 and v = 3x + 1.")

                    st.rerun()

    # CHALLENGE 2 (Shelf 2 - Quotient Rule)
    elif st.session_state.question_number == 1:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">SHELF 2 OF 3 — QUOTIENT RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = \frac{x}{x + 1}")

            answer = st.text_input("YOUR ANSWER (e.g. 1/(x+2)^2)", key="r3_answer2")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if clean_answer(answer) in ["1/(x+1)^2", "1/(1+x)^2", "1/(x+1)²"]:
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
                        use_hint("Quotient Rule: (u/v)' = (u'v - uv') / v^2. Let u = x and v = x + 1.")

                    st.rerun()

    # CHALLENGE 3 (Shelf 3 - Chain Rule)
    elif st.session_state.question_number == 2:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">SHELF 3 OF 3 — CHAIN RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = (2x + 3)^4")

            answer = st.text_input("YOUR ANSWER (e.g. 6(3x+1)^1)", key="r3_answer3")

            left, right = st.columns(2)

            with left:
                if st.button("SUBMIT ANSWER", type="primary", use_container_width=True):

                    if clean_answer(answer) in ["8(2x+3)^3", "8(3+2x)^3"]:
                        st.session_state.feedback = "correct"
                        st.session_state.notification = "✓ CORRECT ANSWER!"
                        st.session_state.notification_type = "success"
                    else:
                        wrong_answer()
                        st.session_state.feedback = "wrong"
                        st.session_state.notification = "✕ INCORRECT ANSWER!"
                        st.session_state.notification_type = "error"

                    st.rerun()

            with right:
                if st.button("USE HINT", type="secondary", use_container_width=True):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint("Chain Rule: differentiate the outer power first, then multiply by the derivative of the inside (2x + 3).")

                    st.rerun()

    # FEEDBACK
    if st.session_state.feedback == "correct":

        st.success("Correct! You found the hidden book.")

        if st.button("CONTINUE", type="primary"):
            st.session_state.notification = ""
            st.session_state.notification_type = ""

            st.session_state.question_number += 1
            st.session_state.feedback = ""
            st.session_state.hint_message = ""
            st.session_state.hint_used_this_question = False

            if st.session_state.question_number == 3:

                st.session_state.room3_cleared = True
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
    
elif st.session_state.page == "room3":
    room3()
