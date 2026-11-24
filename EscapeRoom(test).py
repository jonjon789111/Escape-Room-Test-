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
    "time_limit": 1200,
    "start_time": None,
    "question_number": 0,
    "current_object": None,
    
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
    "hint_used_this_question": False,
    "answer_history": [],
    "wrong_answers": 0,
    "hints_used": 0,
    "end_time": None,
    
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


def presenter_mode():

    if "presenter_unlocked" not in st.session_state:
        st.session_state.presenter_unlocked = False

    with st.sidebar:

        # PRESENTER MODE DESIGN
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #172554, #1e40af);
                padding: 14px;
                border-radius: 12px;
                margin-bottom: 15px;
                border: 1px solid #3b82f6;
            ">
                <div style="font-size: 20px; font-weight: bold; color: white;">
                    🎮 Presenter Mode
                </div>
                <div style="font-size: 11px; color: #bfdbfe;">
                    THE LOCKED CLASSROOM
                </div>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.presenter_unlocked:

            st.caption("🔐 PRESENTER ACCESS")

            password = st.text_input(
                "Enter password",
                type="password",
                key="presenter_password"
            )

            if st.button(
                "Unlock Presenter Mode",
                use_container_width=True
            ):
                if password == st.secrets["PRESENTER_PASSWORD"]:
                    st.session_state.presenter_unlocked = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")

        else:

            st.success("Presenter Mode Active")

            st.markdown("##### 🏫 ROOM NAVIGATION")

            pages = {
                "01 | Blackboard": "room1",
                "02 | Teacher's Desk": "room2",
                "03 | Library": "room3",
                "04 | Exit Door": "room4"
            }

            for name, page in pages.items():

                if st.button(name, use_container_width=True):

                    start_presenter_room(page)

            st.markdown("##### 📂 OTHER PAGES")

            other_pages = {
                "🏠 Home Page": "home",
                "📖 Story": "story",
                "🏆 Achievements": "achievements",
                "📋 Answer History": "review"
            }

            for name, page in other_pages.items():

                if st.button(name, use_container_width=True):

                    st.session_state.page = page
                    st.rerun()

            st.divider()

            if st.button(
                "🔒 Exit Presenter Mode",
                use_container_width=True,
                type="secondary"
            ):
                reset_game()
            
                st.session_state.presenter_unlocked = False
                st.session_state.page = "home"
            
                st.rerun()
                            
# ==========================================
# GAME FUNCTIONS
# ==========================================

def reset_game():

    # GENERAL GAME RESET
    st.session_state.lives = 3
    st.session_state.hints = 2
    st.session_state.time_limit = 1200
    st.session_state.start_time = None
    st.session_state.question_number = 0
    st.session_state.current_object = None

    # ROOM-SPECIFIC STATES
    st.session_state.room2_object = None
    st.session_state.room3_object = None
    st.session_state.room3_completed = []

    # ROOM PROGRESS
    st.session_state.room1_cleared = False
    st.session_state.room2_cleared = False
    st.session_state.room3_cleared = False
    st.session_state.room4_cleared = False

    # KEY COLLECTION
    st.session_state.keys_collected = []

    # GAME STATUS
    st.session_state.game_over = False
    st.session_state.feedback = ""
    st.session_state.hint_message = ""
    st.session_state.hint_used_this_question = False
    st.session_state.answer_history = []
    st.session_state.wrong_answers = 0
    st.session_state.hints_used = 0
    st.session_state.end_time = None

    # NOTIFICATIONS
    st.session_state.notification = ""
    st.session_state.notification_type = ""

    # RESET ANSWER INPUTS
    answer_keys = [
        "answer1", "answer2", "answer3",
        "r2_answer1", "r2_answer2", "r2_answer3",
        "r3_answer1", "r3_answer2", "r3_answer3",
        "r4_answer1", "r4_answer2", "r4_answer3"
    ]

    for key in answer_keys:
        st.session_state.pop(key, None)

def start_presenter_room(room):

    reset_game()

    st.session_state.page = room

    # Start the timer immediately
    st.session_state.start_time = time.time()

    st.rerun()
    
def start_game():

    reset_game()
    st.session_state.start_time = time.time()
    st.session_state.page = "room1"
    
def wrong_answer():

    st.session_state.lives -= 1
    st.session_state.wrong_answers += 1

    if "start_time" in st.session_state:
        st.session_state.start_time -= 5

    if st.session_state.lives <= 0:
        st.session_state.game_over = True

def save_attempt(room, challenge, question, answer, correct_answer, is_correct):

    attempt = {
        "room": room,
        "challenge": challenge,
        "question": question,
        "your_answer": answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct
    }

    st.session_state.answer_history.append(attempt)
        
def use_hint(message):

    if st.session_state.hint_used_this_question:
        st.warning("You already used a hint for this question.")

    elif st.session_state.hints > 0:
        st.session_state.hints -= 1
        st.session_state.hint_used_this_question = True
        st.session_state.hint_message = message
        st.session_state.hints_used += 1

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
            st.caption("Room 4 — Trigonometric Derivative, Exponential Function")

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
        ("ROOM 04", "EXIT DOOR", "Trigonometric Derivatives, Exponential Function")
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
    
    if st.session_state.get("room1_cleared", False):

        # LOAD BRONZE KEY IMAGE
        with open("bronze.png", "rb") as image_file:
            bronze = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        # COMPLETION SCREEN DESIGN
        completion_html = """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

        .completed-room {
            background:
                radial-gradient(
                    circle at top,
                    #49351F 0%,
                    #241A12 55%,
                    #130E0A 100%
                );

            border: 3px double #C69A55;
            outline: 2px solid #634322;
            outline-offset: 5px;

            border-radius: 12px;
            padding: 45px 25px;
            margin: 25px 0;

            text-align: center;

            box-shadow:
                inset 0 0 30px rgba(0,0,0,0.8),
                0 0 25px rgba(198,154,85,0.2);
        }

        .completed-label {
            font-family: 'Cinzel', Georgia, serif;
            color: #D6AD6C;
            font-size: 17px;
            letter-spacing: 5px;
            font-weight: bold;
        }

        .completed-title {
            font-family: 'Cinzel', Georgia, serif;
            color: #FFE3A6;
            font-size: 38px;
            font-weight: 900;
            letter-spacing: 3px;
            margin: 12px 0;
            text-shadow: 0 3px 10px #000;
        }

        .completed-subtitle {
            color: #C7B18E;
            font-size: 15px;
            letter-spacing: 1px;
        }

        .bronze-key {
            margin: 25px 0 10px 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .key-image {
            width: 220px;
            height: auto;
            display: block;
            object-fit: contain;

            filter: drop-shadow(
                0 0 15px rgba(255,190,75,0.5)
            );
        }

        .key-title {
            font-family: 'Cinzel', Georgia, serif;
            color: #E9BE73;
            font-size: 23px;
            font-weight: 900;
            letter-spacing: 2px;
        }

        .completed-progress {
            display: inline-block;
            margin-top: 25px;
            padding: 12px 25px;

            border: 1px solid #89663D;
            background: rgba(0,0,0,0.3);
            border-radius: 6px;

            color: #E8D1A8;
            font-family: 'Cinzel', Georgia, serif;
            font-size: 14px;
            letter-spacing: 2px;
        }

        </style>

        <div class="completed-room">

            <div class="completed-label">
                CHAPTER 01
            </div>

            <div class="completed-title">
                CLASSROOM CLEARED
            </div>

            <div class="completed-subtitle">
                THE BLACKBOARD — LIMITS
            </div>

            <div class="bronze-key">
                <img
                    src="BRONZE_IMAGE_HERE"
                    class="key-image"
                >
            </div>

            <div class="key-title">
                BRONZE KEY ACQUIRED
            </div>

            <div class="completed-subtitle">
                The secrets of the classroom have been uncovered.
            </div>

            <div class="completed-progress">
                3 / 3 CHALLENGES COMPLETED
            </div>

        </div>
        """

        # INSERT THE ACTUAL IMAGE DATA
        completion_html = completion_html.replace(
            "BRONZE_IMAGE_HERE",
            "data:image/png;base64," + bronze
        )

        st.html(completion_html)

        # RETURN BUTTON DESIGN
        st.html("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

        div[class*="st-key-room1_completed_return"] button {

            background: linear-gradient(
                180deg,
                #D9B36C,
                #94652D,
                #583716
            ) !important;

            color: #FFF1D0 !important;
            border: 2px solid #F1D49B !important;
            border-radius: 7px !important;

            min-height: 60px !important;

            font-family: 'Cinzel', Georgia, serif !important;
            font-size: 18px !important;
            font-weight: 900 !important;
            letter-spacing: 2px !important;

            box-shadow:
                0 0 0 3px #352316,
                inset 0 2px 5px #FFE2A4,
                0 0 15px rgba(220,170,90,0.3) !important;

            transition: all 0.25s ease !important;
        }

        div[class*="st-key-room1_completed_return"] button:hover {
            filter: brightness(1.2) !important;
            transform: translateY(-3px) !important;
        }

        </style>
        """)

        # RETURN TO STORY BUTTON
        _, center, _ = st.columns([1, 2, 1])

        with center:

            if st.button(
                "RETURN TO STORY",
                key="room1_completed_return",
                use_container_width=True
            ):

                st.session_state.page = "story"
                st.rerun()

        st.stop()



    header(
        "ROOM 01",
        "THE BLACKBOARD",
        "The first challenge — Limits"
    )

    # INITIALIZE CLASSROOM OBJECT
    if "current_object" not in st.session_state:
        st.session_state.current_object = None

    # GAME OVER
    if st.session_state.game_over:

        st.error("GAME OVER! You ran out of lives or time.")

        if st.button("RETURN TO MENU"):
            reset_game()
            st.session_state.page = "home"
            st.rerun()

        return

    # GAME STATUS
    game_status()
    progress_bar()
    floating_notification()
    key_inventory()

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True
    )

    
   
    # ==========================================
    # CLASSROOM EXPLORATION
    # ==========================================

    if st.session_state.current_object is None:

        st.markdown("### 🔎 EXPLORE THE CLASSROOM")
        st.write("Investigate the objects to uncover hidden challenges.")

        q = st.session_state.question_number

        # BUTTON DESIGN
        
        st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

        /* =====================================
           BASE BUTTON DESIGN - AVAILABLE (RED)
        ===================================== */

        div[class*="st-key-explore_blackboard"] button,
        div[class*="st-key-explore_notebook"] button,
        div[class*="st-key-explore_notes"] button {

            background: linear-gradient(
                180deg,
                #FF7545 0%,
                #D52D12 45%,
                #761204 100%
            ) !important;

            background-color: #B51F08 !important;
            color: #FFF0D0 !important;

            border: 3px double #E6AD65 !important;
            border-radius: 8px !important;

            height: 175px !important;
            min-height: 175px !important;

            font-family: 'Cinzel', Georgia, serif !important;
            font-size: 29px !important;
            font-weight: 900 !important;
            letter-spacing: 2px !important;

            box-shadow:
                0 0 0 3px #302016,
                0 0 0 5px #89633B,
                inset 0 2px 5px #FFD58A,
                inset 0 -5px 8px #4A1300,
                0 0 15px rgba(255,75,0,0.45) !important;

            transition: all 0.25s ease !important;
        }

        /* =====================================
           LOCKED BUTTON - DARK
        ===================================== */

        div[class*="st-key-explore_blackboard"] button:disabled,
        div[class*="st-key-explore_notebook"] button:disabled,
        div[class*="st-key-explore_notes"] button:disabled {

            background: linear-gradient(
                180deg,
                #51433A,
                #29201B,
                #17110E
            ) !important;

            background-color: #29201B !important;
            color: #A99B87 !important;

            border-color: #62513D !important;

            opacity: 0.7 !important;
            filter: grayscale(0.5) !important;
        }

        /* =====================================
           HOVER EFFECT
        ===================================== */

        div[class*="st-key-explore_blackboard"] button:not(:disabled):hover,
        div[class*="st-key-explore_notebook"] button:not(:disabled):hover,
        div[class*="st-key-explore_notes"] button:not(:disabled):hover {

            filter: brightness(1.25) !important;
            transform: translateY(-4px) !important;

            box-shadow:
                0 0 0 3px #302016,
                0 0 0 5px #E6AD65,
                inset 0 2px 5px #FFD58A,
                0 0 22px rgba(255,150,50,0.7) !important;
        }

        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="large")

        # BLACKBOARD
        with col1:

            completed = q >= 1

            if st.button(
                "🖍️  BLACKBOARD",
                type="secondary",
                use_container_width=True,
                key="explore_blackboard"
            ):
                if completed:
                    st.info("You have already completed this challenge.")
                else:
                    st.session_state.current_object = "blackboard"
                    st.rerun()

            if completed:
                st.caption("✓ COMPLETED")
            else:
                st.caption("● AVAILABLE")

        # OLD NOTEBOOK
        with col2:

            completed = q >= 2
            locked = q < 1

            if st.button(
                "📓  OLD NOTEBOOK",
                type="secondary",
                disabled=locked,
                use_container_width=True,
                key="explore_notebook"
            ):
                if completed:
                    st.info("You have already completed this challenge.")
                else:
                    st.session_state.current_object = "notebook"
                    st.rerun()

            if completed:
                st.caption("✓ COMPLETED")
            elif locked:
                st.caption("🔒 LOCKED")
            else:
                st.caption("● AVAILABLE")

        # WALL NOTES
        with col3:

            completed = q >= 3
            locked = q < 2

            if st.button(
                "📌  WALL NOTES",
                type="secondary",
                disabled=locked,
                use_container_width=True,
                key="explore_notes"
            ):
                if completed:
                    st.info("You have already completed this challenge.")
                else:
                    st.session_state.current_object = "notes"
                    st.rerun()

            if completed:
                st.caption("✓ COMPLETED")
            elif locked:
                st.caption("🔒 LOCKED")
            else:
                st.caption("● AVAILABLE")

    # ==========================================
    # CHALLENGE 1 — BLACKBOARD
    # ==========================================

    elif st.session_state.current_object == "blackboard":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">CHALLENGE 1 OF 3</div>',
                unsafe_allow_html=True
            )

            st.markdown("### 🖍️ Blackboard")

            st.write("Find the limit:")

            st.latex(r"\lim_{x\to2}(3x+4)")

            answer = st.text_input(
                "YOUR ANSWER",
                key="answer1"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    type="primary",
                    use_container_width=True
                ):

                    is_correct = answer.strip() == "10"

                    save_attempt(
                        "ROOM 1 - BLACKBOARD",
                        1,
                        r"\lim_{x\to2}(3x+4)",
                        answer,
                        "10",
                        is_correct
                    )

                    if is_correct:

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

                if st.button(
                    "USE HINT",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:

                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:

                        use_hint(
                            "Substitute x = 2 into the expression."
                        )

                    st.rerun()

    # ==========================================
    # CHALLENGE 2 — TEACHER'S DESK
    # ==========================================

    elif st.session_state.current_object == "notebook":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">CHALLENGE 2 OF 3</div>',
                unsafe_allow_html=True
            )

            st.markdown("### 📓 Old Notebook")

            st.write("Evaluate the following limit:")

            st.latex(r"\lim_{x\to2}\frac{x^2-4}{x-2}")

            answer = st.text_input(
                "YOUR ANSWER",
                key="answer2"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    type="primary",
                    use_container_width=True
                ):

                    is_correct = answer.strip() == "4"

                    save_attempt(
                        "ROOM 1 - BLACKBOARD",
                        2,
                        r"\lim_{x\to2}\frac{x^2-4}{x-2}",
                        answer,
                        "4",
                        is_correct
                    )

                    if is_correct:

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

                if st.button(
                    "USE HINT",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:

                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:

                        use_hint(
                            "Factor the numerator into (x - 2)(x + 2)."
                        )

                    st.rerun()

    # ==========================================
    # CHALLENGE 3 — WALL NOTES
    # ==========================================

    elif st.session_state.current_object == "notes":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">CHALLENGE 3 OF 3</div>',
                unsafe_allow_html=True
            )

            st.markdown("### 📌 Wall Notes")

            st.write("Find the limit:")

            st.latex(r"\lim_{x\to1}\frac{x^2+3x-4}{x-1}")

            answer = st.text_input(
                "YOUR ANSWER",
                key="answer3"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    type="primary",
                    use_container_width=True
                ):

                    is_correct = answer.strip() == "5"

                    save_attempt(
                        "ROOM 1 - BLACKBOARD",
                        3,
                        r"\lim_{x\to1}\frac{x^2+3x-4}{x-1}",
                        answer,
                        "5",
                        is_correct
                    )

                    if is_correct:

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

                if st.button(
                    "USE HINT",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:

                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:

                        use_hint(
                            "Factor the numerator into (x - 1)(x + 4)."
                        )

                    st.rerun()

    # ==========================================
    # FEEDBACK
    # ==========================================

    if st.session_state.feedback == "correct":

        st.success("Correct! You solved the challenge.")

        if st.button("CONTINUE", type="primary"):

            st.session_state.notification = ""
            st.session_state.notification_type = ""

            st.session_state.question_number += 1
            st.session_state.feedback = ""
            st.session_state.hint_message = ""
            st.session_state.hint_used_this_question = False

            # RETURN TO CLASSROOM EXPLORATION
            st.session_state.current_object = None

            # ROOM COMPLETED
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

    # ==========================================
    # HINT MESSAGE
    # ==========================================

    if st.session_state.hint_message:

        st.info(st.session_state.hint_message)

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True
    )


# ==========================================
# ROOM 2 — THE TEACHER'S DESK
# ==========================================

def room2():

    design()

    # ==========================================
    # ROOM 2 COMPLETION SCREEN
    # ==========================================

    if st.session_state.get("room2_cleared", False):

        # LOAD SILVER KEY IMAGE
        with open("silver.png", "rb") as image_file:
            silver = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        # COMPLETION SCREEN DESIGN
        completion_html = """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

        .completed-room {
            background:
                radial-gradient(
                    circle at top,
                    #49351F 0%,
                    #241A12 55%,
                    #130E0A 100%
                );

            border: 3px double #C69A55;
            outline: 2px solid #634322;
            outline-offset: 5px;

            border-radius: 12px;
            padding: 45px 25px;
            margin: 25px 0;

            text-align: center;

            box-shadow:
                inset 0 0 30px rgba(0,0,0,0.8),
                0 0 25px rgba(198,154,85,0.2);
        }

        .completed-label {
            font-family: 'Cinzel', Georgia, serif;
            color: #D6AD6C;
            font-size: 17px;
            letter-spacing: 5px;
            font-weight: bold;
        }

        .completed-title {
            font-family: 'Cinzel', Georgia, serif;
            color: #FFE3A6;
            font-size: 38px;
            font-weight: 900;
            letter-spacing: 3px;
            margin: 12px 0;
            text-shadow: 0 3px 10px #000;
        }

        .completed-subtitle {
            color: #C7B18E;
            font-size: 15px;
            letter-spacing: 1px;
        }

        .silver-key {
            margin: 25px 0 10px 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .key-image {
            width: 220px;
            height: auto;
            display: block;
            object-fit: contain;

            filter: drop-shadow(
                0 0 15px rgba(190,215,255,0.5)
            );
        }

        .key-title {
            font-family: 'Cinzel', Georgia, serif;
            color: #DCE8F5;
            font-size: 23px;
            font-weight: 900;
            letter-spacing: 2px;
        }

        .completed-progress {
            display: inline-block;
            margin-top: 25px;
            padding: 12px 25px;

            border: 1px solid #89663D;
            background: rgba(0,0,0,0.3);
            border-radius: 6px;

            color: #E8D1A8;
            font-family: 'Cinzel', Georgia, serif;
            font-size: 14px;
            letter-spacing: 2px;
        }

        </style>

        <div class="completed-room">

            <div class="completed-label">
                CHAPTER 02
            </div>

            <div class="completed-title">
                CLASSROOM CLEARED
            </div>

            <div class="completed-subtitle">
                THE TEACHER'S DESK — BASIC DERIVATIVES
            </div>

            <div class="silver-key">
                <img
                    src="SILVER_IMAGE_HERE"
                    class="key-image"
                >
            </div>

            <div class="key-title">
                SILVER KEY ACQUIRED
            </div>

            <div class="completed-subtitle">
                The knowledge hidden within the desk has been uncovered.
            </div>

            <div class="completed-progress">
                3 / 3 CHALLENGES COMPLETED
            </div>

        </div>
        """

        # INSERT THE ACTUAL IMAGE DATA
        completion_html = completion_html.replace(
            "SILVER_IMAGE_HERE",
            "data:image/png;base64," + silver
        )

        st.html(completion_html)

        # RETURN BUTTON DESIGN
        st.html("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

        div[class*="st-key-room2_completed_return"] button {

            background: linear-gradient(
                180deg,
                #D9B36C,
                #94652D,
                #583716
            ) !important;

            color: #FFF1D0 !important;
            border: 2px solid #F1D49B !important;
            border-radius: 7px !important;

            min-height: 60px !important;

            font-family: 'Cinzel', Georgia, serif !important;
            font-size: 18px !important;
            font-weight: 900 !important;
            letter-spacing: 2px !important;

            box-shadow:
                0 0 0 3px #352316,
                inset 0 2px 5px #FFE2A4,
                0 0 15px rgba(220,170,90,0.3) !important;

            transition: all 0.25s ease !important;
        }

        div[class*="st-key-room2_completed_return"] button:hover {
            filter: brightness(1.2) !important;
            transform: translateY(-3px) !important;
        }

        </style>
        """)

        # RETURN TO STORY BUTTON
        _, center, _ = st.columns([1, 2, 1])

        with center:

            if st.button(
                "RETURN TO STORY",
                key="room2_completed_return",
                use_container_width=True
            ):

                st.session_state.page = "story"
                st.rerun()

        st.stop()

    # ==========================================
    # INITIALIZE ROOM STATE
    # ==========================================

    if "room2_object" not in st.session_state:
        st.session_state.room2_object = None

    header(
        "ROOM 02",
        "THE TEACHER'S DESK",
        "The second challenge — Basic Derivatives"
    )

    if st.session_state.game_over:

        st.error("GAME OVER! You ran out of lives or time.")

        if st.button("RETURN TO MENU", key="r2_gameover_menu"):
            reset_game()
            st.session_state.page = "home"
            st.rerun()

        return

    game_status()
    progress_bar()
    floating_notification()
    key_inventory()

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    # ==========================================
    # DRAWER BUTTON DESIGN
    # ==========================================

    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

        div[class*="st-key-r2_drawer"] button {

            min-height:115px !important;
            border-radius:10px !important;
            border:3px double #C69A55 !important;

            font-family:'Cinzel', Georgia, serif !important;
            font-size:19px !important;
            font-weight:900 !important;
            letter-spacing:1px !important;

            box-shadow:
                inset 0 2px 5px rgba(255,255,255,0.12),
                inset 0 -5px 10px rgba(0,0,0,0.35),
                0 5px 12px rgba(0,0,0,0.4) !important;

            transition:all 0.25s ease !important;
        }

        div[class*="st-key-r2_drawer"] button[kind="primary"] {

            background:linear-gradient(
                145deg,
                #A52D24,
                #762019,
                #48130F
            ) !important;

            color:#FFE5C2 !important;
            border-color:#D9A45B !important;
        }

        div[class*="st-key-r2_drawer"] button:disabled {

            background:linear-gradient(
                145deg,
                #39302A,
                #211B17
            ) !important;

            color:#887B6A !important;
            border-color:#67513A !important;
            opacity:0.75 !important;
        }

        div[class*="st-key-r2_drawer"] button:not(:disabled):hover {

            transform:translateY(-4px) !important;

            box-shadow:
                0 0 15px rgba(205,155,78,0.4),
                inset 0 2px 5px rgba(255,255,255,0.2) !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ==========================================
    # DRAWER SELECTION
    # ==========================================

    if st.session_state.room2_object is None:

        q = st.session_state.question_number

        st.markdown(
            """
            <h2 style="
                text-align:center;
                font-family:'Cinzel', Georgia, serif;
                color:#E5C58B;
                letter-spacing:3px;
                font-size:27px;
                margin:25px 0;
            ">
                THE TEACHER'S DESK
            </h2>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            label1 = "✓ DRAWER 01" if q >= 1 else "DRAWER 01"

            if st.button(
                label1,
                key="r2_drawer1",
                type="primary",
                use_container_width=True
            ):

                if q == 0:
                    st.session_state.room2_object = "drawer1"
                    st.rerun()

                else:
                    st.info("You have already completed this drawer.")

        with col2:

            if q >= 2:
                label2 = "✓ DRAWER 02"
            elif q < 1:
                label2 = "🔒 DRAWER 02"
            else:
                label2 = "DRAWER 02"

            if st.button(
                label2,
                key="r2_drawer2",
                type="primary" if q >= 1 else "secondary",
                disabled=q < 1,
                use_container_width=True
            ):

                if q == 1:
                    st.session_state.room2_object = "drawer2"
                    st.rerun()

                else:
                    st.info("You have already completed this drawer.")

        with col3:

            if q >= 3:
                label3 = "✓ DRAWER 03"
            elif q < 2:
                label3 = "🔒 DRAWER 03"
            else:
                label3 = "DRAWER 03"

            if st.button(
                label3,
                key="r2_drawer3",
                type="primary" if q >= 2 else "secondary",
                disabled=q < 2,
                use_container_width=True
            ):

                if q == 2:
                    st.session_state.room2_object = "drawer3"
                    st.rerun()

                else:
                    st.info("You have already completed this drawer.")

    # ==========================================
    # CHALLENGE 1 — POWER RULE
    # ==========================================

    elif st.session_state.room2_object == "drawer1" and st.session_state.question_number == 0:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">DRAWER 1 OF 3 — POWER RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = 4x^3")

            answer = st.text_input(
                "YOUR ANSWER (e.g. 2x^2)",
                key="r2_answer1"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    key="r2_submit1",
                    type="primary",
                    use_container_width=True
                ):

                    normalized = answer.replace(" ", "").replace("**", "^").replace("*", "").lower()
                    is_correct = normalized == "12x^2"

                    save_attempt(
                        "ROOM 2 - TEACHER'S DESK",
                        1,
                        "f(x) = 4x^3",
                        answer,
                        "12x^2",
                        is_correct
                    )

                    if is_correct:
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

                if st.button(
                    "USE HINT",
                    key="r2_hint1",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint(
                            "Apply the Power Rule: bring down the exponent 3, multiply by 4, and subtract 1 from the exponent."
                        )

                    st.rerun()

    # ==========================================
    # CHALLENGE 2 — SUM AND DIFFERENCE RULES
    # ==========================================

    elif st.session_state.room2_object == "drawer2" and st.session_state.question_number == 1:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">DRAWER 2 OF 3 — SUM & DIFFERENCE RULES</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = 5x^2 - 3x + 7")

            answer = st.text_input(
                "YOUR ANSWER",
                key="r2_answer2"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    key="r2_submit2",
                    type="primary",
                    use_container_width=True
                ):

                    normalized = answer.replace(" ", "").replace("**", "^").replace("*", "").lower()
                    is_correct = normalized == "10x-3"

                    save_attempt(
                        "ROOM 2 - TEACHER'S DESK",
                        2,
                        "f(x) = 5x^2 - 3x + 7",
                        answer,
                        "10x-3",
                        is_correct
                    )

                    if is_correct:
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

                if st.button(
                    "USE HINT",
                    key="r2_hint2",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint(
                            "Differentiate each term separately. Remember that the derivative of a constant (7) is 0."
                        )

                    st.rerun()

    # ==========================================
    # CHALLENGE 3 — COMBINATION OF BASIC RULES
    # ==========================================

    elif st.session_state.room2_object == "drawer3" and st.session_state.question_number == 2:

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">DRAWER 3 OF 3 — COMBINATION OF BASIC RULES</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = 10x^4 + 9x^3 + 4x^2 + x + 67")

            answer = st.text_input(
                "YOUR ANSWER",
                key="r2_answer3"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    key="r2_submit3",
                    type="primary",
                    use_container_width=True
                ):

                    normalized = answer.replace(" ", "").replace("**", "^").replace("*", "").lower()
                    is_correct = normalized == "40x^3+27x^2+8x+1"

                    save_attempt(
                        "ROOM 2 - TEACHER'S DESK",
                        3,
                        "f(x) = 10x^4 + 9x^3 + 4x^2 + x + 67",
                        answer,
                        "40x^3+27x^2+8x+1",
                        is_correct
                    )

                    if is_correct:
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

                if st.button(
                    "USE HINT",
                    key="r2_hint3",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = "You can only use a hint once per challenge!"

                    else:
                        use_hint(
                            "Apply the Power Rule to each term: the derivative of x is 1, and the derivative of 67 is 0."
                        )

                    st.rerun()

    # ==========================================
    # RETURN TO DRAWERS
    # ==========================================

    if st.session_state.room2_object is not None:

        if st.button("← BACK TO DRAWERS", key="r2_back_to_drawers"):

            if st.session_state.feedback == "correct":
                st.warning("Press CONTINUE first to save your progress.")

            else:
                st.session_state.room2_object = None
                st.rerun()

    # ==========================================
    # FEEDBACK
    # ==========================================

    if st.session_state.feedback == "correct":

        st.success("Correct! You solved the challenge.")

        if st.button("CONTINUE", key="r2_continue", type="primary"):

            st.session_state.notification = ""
            st.session_state.notification_type = ""

            st.session_state.question_number += 1
            st.session_state.feedback = ""
            st.session_state.hint_message = ""
            st.session_state.hint_used_this_question = False
            st.session_state.room2_object = None

            if st.session_state.question_number == 3:

                st.session_state.room2_cleared = True

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

    # ==========================================
    # HINT MESSAGE
    # ==========================================

    if st.session_state.hint_message:
        st.info(st.session_state.hint_message)

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
   
def room3():

    design()
    
    # INITIALIZE ROOM 3 STATES
    if "room3_object" not in st.session_state:
        st.session_state.room3_object = None

    if "room3_completed" not in st.session_state:
        st.session_state.room3_completed = []

    # ROOM 3 COMPLETION SCREEN
    # Only appears when the player enters Room 3 again.
    if st.session_state.get("room3_cleared", False):

        with open("gold.png", "rb") as image_file:
            gold = base64.b64encode(image_file.read()).decode("utf-8")

        completion_html = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

        .completed-room {
            background: radial-gradient(circle at top, #49351F 0%, #241A12 55%, #130E0A 100%);
            border: 3px double #C69A45;
            border-radius: 18px;
            padding: 35px 20px;
            text-align: center;
            box-shadow: 0 0 25px rgba(198,154,69,0.25);
            margin-top: 15px;
            margin-bottom: 20px;
        }

        .completed-room .chapter {
            color: #D6B56D;
            font-family: 'Cinzel', serif;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 5px;
        }

        .completed-room .main-title {
            color: #F4D58D;
            font-family: 'Cinzel', serif;
            font-size: 35px;
            font-weight: 900;
            margin: 12px 0;
        }

        .completed-room .room-name {
            color: #D9C39A;
            font-family: 'Cinzel', serif;
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 20px;
        }

        .completed-room .key-image {
            width: 220px;
            max-width: 75%;
            margin: 10px auto;
            filter: drop-shadow(0 0 18px rgba(255,190,65,0.45));
        }

        .completed-room .key-title {
            color: #E7BD60;
            font-family: 'Cinzel', serif;
            font-size: 25px;
            font-weight: 900;
            margin-top: 12px;
        }

        .completed-room .description {
            color: #E2D3B8;
            font-size: 15px;
            margin-top: 12px;
        }

        .completed-room .progress-text {
            color: #D6B56D;
            font-family: 'Cinzel', serif;
            font-weight: 800;
            font-size: 14px;
            letter-spacing: 2px;
            margin-top: 25px;
        }
        </style>

        <div class="completed-room">
            <div class="chapter">CHAPTER 03</div>
            <div class="main-title">CLASSROOM CLEARED</div>
            <div class="room-name">
                THE LIBRARY — PRODUCT, QUOTIENT & CHAIN RULES
            </div>
            <img class="key-image" src="GOLD_IMAGE_HERE">
            <div class="key-title">GOLD KEY ACQUIRED</div>
            <div class="description">
                The secrets hidden within the library have been uncovered.
            </div>
            <div class="progress-text">
                3 / 3 CHALLENGES COMPLETED
            </div>
        </div>
        """

        completion_html = completion_html.replace(
            "GOLD_IMAGE_HERE",
            "data:image/png;base64," + gold
        )

        st.html(completion_html)

        st.html("""
        <style>
        div[class*="st-key-room3_completed_return"] button {
            background: linear-gradient(135deg, #D5A744, #8C5D1C) !important;
            color: #211609 !important;
            border: 2px solid #F0D18A !important;
            border-radius: 12px !important;
            font-family: 'Cinzel', serif !important;
            font-weight: 900 !important;
            letter-spacing: 2px !important;
            min-height: 52px !important;
        }

        div[class*="st-key-room3_completed_return"] button:hover {
            background: linear-gradient(135deg, #F0D18A, #C18A2D) !important;
            border-color: #FFF0C2 !important;
        }
        </style>
        """)

        _, center, _ = st.columns([1, 2, 1])

        with center:
            if st.button(
                "RETURN TO STORY",
                key="room3_completed_return",
                use_container_width=True
            ):
                st.session_state.page = "story"
                st.rerun()

        st.stop()

    # ROOM DESIGN

    header(
        "ROOM 03",
        "THE LIBRARY",
        "The third challenge — Product, Quotient & Chain Rules"
    )

    # GAME OVER CHECK
    if st.session_state.game_over:

        st.error("GAME OVER! You ran out of lives or time.")

        if st.button("RETURN TO MENU"):
            st.session_state.page = "home"
            st.rerun()

        return

    # GAME INFORMATION
    game_status()
    progress_bar()
    floating_notification()
    key_inventory()

    # SHELF BUTTON DESIGN
    st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

    div[class*="st-key-room3_shelf"] button {
        background:
            linear-gradient(145deg, #49301E, #2B1B12 55%, #190F09) !important;
        border: 2px solid #A77B3D !important;
        border-radius: 10px !important;
        min-height: 78px !important;
        color: #F0D6A0 !important;
        font-family: 'Cinzel', serif !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        box-shadow:
            inset 0 1px 0 rgba(255,225,170,0.18),
            inset 0 0 0 4px rgba(198,154,69,0.08),
            0 6px 15px rgba(0,0,0,0.45) !important;
        transition: all 0.25s ease !important;
    }

    div[class*="st-key-room3_shelf"] button:hover {
        background: linear-gradient(135deg, #73502A, #3F2918, #604323) !important;
        border-color: #F0D18A !important;
        color: #FFF0C2 !important;
        box-shadow: 0 0 20px rgba(218,165,72,0.35) !important;
        transform: translateY(-3px);
    }
    </style>
    """)

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True
    )

    # CHALLENGE SELECTION SCREEN
    if st.session_state.room3_object is None:

        st.markdown(
            '<div class="section-title">THE LIBRARY — SELECT A SHELF</div>',
            unsafe_allow_html=True
        )

        st.write("Choose a shelf to begin your challenge.")

        completed = st.session_state.room3_completed

        # SHELF 1 - PRODUCT RULE
        if st.button(
            "📖  SHELF I — THE PRODUCT RULE",
            key="room3_shelf1",
            use_container_width=True
        ):

            if "shelf1" in completed:
                st.warning(
                    "✓ YOU HAVE ALREADY COMPLETED THIS CHALLENGE!"
                )

            else:
                st.session_state.room3_object = "shelf1"
                st.rerun()

        # SHELF 2 - QUOTIENT RULE
        if st.button(
            "📖  SHELF II — THE QUOTIENT RULE",
            key="room3_shelf2",
            use_container_width=True
        ):

            if "shelf2" in completed:
                st.warning(
                    "✓ YOU HAVE ALREADY COMPLETED THIS CHALLENGE!"
                )

            elif "shelf1" not in completed:
                st.warning("🔒 COMPLETE SHELF I FIRST!")

            else:
                st.session_state.room3_object = "shelf2"
                st.rerun()

        # SHELF 3 - CHAIN RULE
        if st.button(
            "📖  SHELF III — THE CHAIN RULE",
            key="room3_shelf3",
            use_container_width=True
        ):

            if "shelf3" in completed:
                st.warning(
                    "✓ YOU HAVE ALREADY COMPLETED THIS CHALLENGE!"
                )

            elif "shelf2" not in completed:
                st.warning("🔒 COMPLETE SHELF II FIRST!")

            else:
                st.session_state.room3_object = "shelf3"
                st.rerun()

        st.markdown(
            '<div class="gold-line"></div>',
            unsafe_allow_html=True
        )

    # CHALLENGE 1 - PRODUCT RULE
    elif st.session_state.room3_object == "shelf1":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">SHELF 1 OF 3 — PRODUCT RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = x^2(3x + 1)")

            answer = st.text_input(
                "YOUR ANSWER",
                key="r3_answer1"
            )

            left, right = st.columns(2)

            with left:
                if st.button(
                    "SUBMIT ANSWER",
                    key="r3_submit1",
                    type="primary",
                    use_container_width=True
                ):

                    normalized_answer = (
                        answer.replace(" ", "")
                        .replace("**", "^")
                        .lower()
                    )

                    is_correct = normalized_answer in [
                        "9x^2+2x",
                        "2x+9x^2"
                    ]

                    save_attempt(
                        "ROOM 3 - LIBRARY",
                        1,
                        "f(x) = x^2(3x + 1)",
                        answer,
                        "9x^2+2x",
                        is_correct
                    )

                    if is_correct:
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
                if st.button(
                    "USE HINT",
                    key="r3_hint1",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:
                        use_hint(
                            "Product Rule: (uv)' = u'v + uv'. "
                            "Let u = x^2 and v = 3x + 1."
                        )

                    st.rerun()

    # CHALLENGE 2 - QUOTIENT RULE
    elif st.session_state.room3_object == "shelf2":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">SHELF 2 OF 3 — QUOTIENT RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = \frac{x}{x + 1}")

            answer = st.text_input(
                "YOUR ANSWER",
                key="r3_answer2"
            )

            left, right = st.columns(2)

            with left:
                if st.button(
                    "SUBMIT ANSWER",
                    key="r3_submit2",
                    type="primary",
                    use_container_width=True
                ):

                    normalized_answer = (
                        answer.replace(" ", "")
                        .replace("**", "^")
                        .lower()
                    )

                    is_correct = normalized_answer in [
                        "1/(x+1)^2",
                        "1/(1+x)^2",
                        "1/(x+1)²"
                    ]

                    save_attempt(
                        "ROOM 3 - LIBRARY",
                        2,
                        "f(x) = x/(x + 1)",
                        answer,
                        "1/(x+1)^2",
                        is_correct
                    )

                    if is_correct:
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
                if st.button(
                    "USE HINT",
                    key="r3_hint2",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:
                        use_hint(
                            "Quotient Rule: (u/v)' = (u'v - uv') / v^2. "
                            "Let u = x and v = x + 1."
                        )

                    st.rerun()

    # CHALLENGE 3 - CHAIN RULE
    elif st.session_state.room3_object == "shelf3":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">SHELF 3 OF 3 — CHAIN RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")
            st.latex(r"f(x) = (2x + 3)^4")

            answer = st.text_input(
                "YOUR ANSWER",
                key="r3_answer3"
            )

            left, right = st.columns(2)

            with left:
                if st.button(
                    "SUBMIT ANSWER",
                    key="r3_submit3",
                    type="primary",
                    use_container_width=True
                ):

                    normalized_answer = (
                        answer.replace(" ", "")
                        .replace("**", "^")
                        .lower()
                    )

                    is_correct = normalized_answer in [
                        "8(2x+3)^3",
                        "8(3+2x)^3"
                    ]

                    save_attempt(
                        "ROOM 3 - LIBRARY",
                        3,
                        "f(x) = (2x + 3)^4",
                        answer,
                        "8(2x+3)^3",
                        is_correct
                    )

                    if is_correct:
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
                if st.button(
                    "USE HINT",
                    key="r3_hint3",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:
                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:
                        use_hint(
                            "Chain Rule: differentiate the outer power first, "
                            "then multiply by the derivative of the inside "
                            "(2x + 3)."
                        )

                    st.rerun()

    # FEEDBACK
    if st.session_state.feedback == "correct":

        st.success("Correct! You completed the challenge.")

        if st.button(
            "CONTINUE",
            key="r3_continue",
            type="primary"
        ):

            current_shelf = st.session_state.room3_object

            # MARK CURRENT SHELF AS COMPLETED
            if current_shelf not in st.session_state.room3_completed:
                st.session_state.room3_completed.append(current_shelf)

            # CLEAR CHALLENGE FEEDBACK
            st.session_state.notification = ""
            st.session_state.notification_type = ""
            st.session_state.feedback = ""
            st.session_state.hint_message = ""
            st.session_state.hint_used_this_question = False

            # RETURN TO SHELF SELECTION
            st.session_state.room3_object = None

            # ALL THREE CHALLENGES COMPLETED
            if len(st.session_state.room3_completed) == 3:

                st.session_state.room3_cleared = True

                if "Gold Key" not in st.session_state.keys_collected:
                    st.session_state.keys_collected.append("Gold Key")

                st.session_state.notification = "🔑 GOLD KEY COLLECTED!"
                st.session_state.notification_type = "warning"

                # RETURN TO STORY PAGE
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

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True
    )


def room4():

    design()

    # ==========================================
    # ROOM 4 INITIALIZATION
    # ==========================================

    if "room4_object" not in st.session_state:
        st.session_state.room4_object = None

    if "room4_completed" not in st.session_state:
        st.session_state.room4_completed = []

    if "room4_notice" not in st.session_state:
        st.session_state.room4_notice = ""

    if "room4_cleared" not in st.session_state:
        st.session_state.room4_cleared = False

    # ==========================================
    # ROOM 4 COMPLETION SCREEN
    # Only appears when revisiting a cleared room
    # ==========================================

    if st.session_state.room4_cleared:

        try:
            with open("crystal.png", "rb") as image_file:
                crystal = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            crystal_image = (
                '<img src="data:image/png;base64,'
                + crystal +
                '" class="key-image">'
            )

        except FileNotFoundError:
            crystal_image = ""

        completion_html = """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&display=swap');

        .completed-room {
            background:
                radial-gradient(circle at top, #49351F 0%, #241A12 55%, #130E0A 100%);
            border: 3px double #D8B66A;
            border-radius: 18px;
            padding: 38px 20px;
            text-align: center;
            color: #F4E6C4;
            box-shadow: 0 0 25px rgba(218, 177, 87, 0.20);
            font-family: 'Cinzel', serif;
        }

        .completed-room .chapter {
            color: #D9B96E;
            font-size: 13px;
            letter-spacing: 5px;
            font-weight: 800;
        }

        .completed-room h1 {
            color: #F8E6B2;
            font-size: 34px;
            font-weight: 900;
            letter-spacing: 3px;
            margin: 12px 0;
        }

        .completed-room .room-name {
            color: #D9B96E;
            font-size: 16px;
            letter-spacing: 2px;
            margin-bottom: 25px;
        }

        .completed-room .key-image {
            width: 145px;
            height: 145px;
            object-fit: contain;
            margin: 12px auto;
            filter: drop-shadow(0 0 15px rgba(130, 210, 255, 0.45));
        }

        .completed-room .key-title {
            color: #A9E3FF;
            font-size: 22px;
            font-weight: 900;
            letter-spacing: 3px;
            margin-top: 10px;
        }

        .completed-room .description {
            color: #D8C9A7;
            font-size: 13px;
            margin: 15px 0;
        }

        .completed-room .progress {
            color: #E8D7AC;
            font-size: 13px;
            letter-spacing: 2px;
            margin-top: 25px;
        }

        </style>

        <div class="completed-room">

            <div class="chapter">FINAL CHAPTER</div>

            <h1>EXIT UNLOCKED</h1>

            <div class="room-name">
                THE EXIT DOOR — FINAL CHALLENGE
            </div>

            CRYSTAL_IMAGE

            <div class="key-title">
                CRYSTAL KEY ACQUIRED
            </div>

            <div class="description">
                You have successfully completed all three locks
                and uncovered the final path.
            </div>

            <div class="progress">
                3 / 3 CHALLENGES COMPLETED
            </div>

        </div>
        """

        completion_html = completion_html.replace(
            "CRYSTAL_IMAGE",
            crystal_image
        )

        st.html(completion_html)

        st.markdown("<br>", unsafe_allow_html=True)

        _, center, _ = st.columns([1, 2, 1])

        with center:

            if st.button(
                "RETURN TO STORY",
                key="room4_completed_return",
                use_container_width=True
            ):
                st.session_state.page = "story"
                st.rerun()

        st.stop()

    # ==========================================
    # ROOM DESIGN
    # ==========================================

    header(
        "ROOM 04",
        "THE EXIT DOOR",
        "The final challenge — Unlock your way out"
    )

    # ==========================================
    # GAME OVER
    # ==========================================

    if st.session_state.game_over:

        st.error("GAME OVER! You ran out of lives or time.")

        if st.button("RETURN TO MENU"):
            st.session_state.page = "home"
            st.rerun()

        return

    # ==========================================
    # GAME STATUS
    # ==========================================

    game_status()
    progress_bar()
    floating_notification()
    key_inventory()

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True
    )

    # ==========================================
    # CHALLENGE SELECTION
    # ==========================================

    if st.session_state.room4_object is None:

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:15px 5px 20px 5px;
            ">
                <h2 style="
                    font-family:Cinzel, serif;
                    color:#E5C77D;
                    letter-spacing:3px;
                ">
                    THE THREE LOCKS
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <style>

            div[class*="st-key-room4_lock"] button {
                background: linear-gradient(
                    145deg,
                    #49351F,
                    #241A12
                );
                border: 2px solid #B99450;
                border-radius: 12px;
                color: #F5E4B8;
                min-height: 105px;
                font-family: Cinzel, serif;
                font-weight: 800;
                letter-spacing: 1px;
                transition: 0.2s ease;
            }

            div[class*="st-key-room4_lock"] button:hover {
                border-color: #FFE09A;
                background: linear-gradient(
                    145deg,
                    #70502A,
                    #342315
                );
                color: #FFFFFF;
                transform: translateY(-3px);
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        # LOCK 1
        with col1:

            if st.button(
                "🔐 LOCK I\n\nTRIGONOMETRIC",
                key="room4_lock1",
                use_container_width=True
            ):

                if "lock1" in st.session_state.room4_completed:

                    st.session_state.room4_notice = (
                        "✓ YOU HAVE ALREADY COMPLETED LOCK 1!"
                    )

                else:

                    st.session_state.room4_notice = ""
                    st.session_state.room4_object = "lock1"
                    st.rerun()

        # LOCK 2
        with col2:

            if st.button(
                "🔐 LOCK II\n\nEXPONENTIAL",
                key="room4_lock2",
                use_container_width=True
            ):

                if "lock2" in st.session_state.room4_completed:

                    st.session_state.room4_notice = (
                        "✓ YOU HAVE ALREADY COMPLETED LOCK 2!"
                    )

                elif "lock1" not in st.session_state.room4_completed:

                    st.session_state.room4_notice = (
                        "🔒 COMPLETE LOCK 1 FIRST!"
                    )

                else:

                    st.session_state.room4_notice = ""
                    st.session_state.room4_object = "lock2"
                    st.rerun()

        # LOCK 3
        with col3:

            if st.button(
                "🔐 LOCK III\n\nPRODUCT RULE",
                key="room4_lock3",
                use_container_width=True
            ):

                if "lock3" in st.session_state.room4_completed:

                    st.session_state.room4_notice = (
                        "✓ YOU HAVE ALREADY COMPLETED LOCK 3!"
                    )

                elif "lock2" not in st.session_state.room4_completed:

                    st.session_state.room4_notice = (
                        "🔒 COMPLETE LOCK 2 FIRST!"
                    )

                else:

                    st.session_state.room4_notice = ""
                    st.session_state.room4_object = "lock3"
                    st.rerun()

        if st.session_state.room4_notice:
            st.warning(st.session_state.room4_notice)

        # LOCK STATUS
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                background:rgba(40,29,18,0.7);
                border:1px solid #806333;
                border-radius:12px;
                padding:15px;
                text-align:center;
                color:#DCC99B;
                font-size:13px;
            ">
                COMPLETE ALL THREE LOCKS TO ESCAPE
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==========================================
    # CHALLENGE 1 — TRIGONOMETRIC
    # ==========================================

    elif st.session_state.room4_object == "lock1":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">LOCK I — TRIGONOMETRIC FUNCTION WITH CHAIN RULE</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")

            st.latex(r"f(x) = \sin(2x)")

            answer = st.text_input(
                "YOUR ANSWER",
                key="r4_answer1"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    key="r4_submit1",
                    type="primary",
                    use_container_width=True
                ):

                    normalized = (
                        answer.lower()
                        .replace(" ", "")
                        .replace("**", "^")
                        .replace("*", "")
                    )

                    is_correct = normalized in [
                        "2cos(2x)",
                        "2cos2x"
                    ]

                    save_attempt(
                        "ROOM 4 - EXIT DOOR",
                        1,
                        "f(x) = sin(2x)",
                        answer,
                        "2cos(2x)",
                        is_correct
                    )

                    if is_correct:

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

                if st.button(
                    "USE HINT",
                    key="r4_hint1",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:

                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:

                        use_hint(
                            "Apply the Chain Rule: differentiate the outer sine function first, then multiply by the derivative of the inner function (2x)."
                        )

                    st.rerun()

    # ==========================================
    # CHALLENGE 2 — EXPONENTIAL
    # ==========================================

    elif st.session_state.room4_object == "lock2":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">LOCK II — EXPONENTIAL FUNCTIONS</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")

            st.latex(r"f(u) = 5^u")

            answer = st.text_input(
                "YOUR ANSWER (e.g. 3^x ln(3))",
                key="r4_answer2"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    key="r4_submit2",
                    type="primary",
                    use_container_width=True
                ):

                    normalized = (
                        answer.lower()
                        .replace(" ", "")
                        .replace("**", "^")
                        .replace("*", "")
                    )

                    is_correct = normalized in [
                        "5^uln(5)"
                    ]

                    save_attempt(
                        "ROOM 4 - EXIT DOOR",
                        2,
                        "f(u) = 5^u",
                        answer,
                        "5^u ln(5)",
                        is_correct
                    )

                    if is_correct:

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

                if st.button(
                    "USE HINT",
                    key="r4_hint2",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:

                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:

                        use_hint(
                            "Formula: d/du(a^u) = a^u ln(a)"
                        )

                    st.rerun()

    # ==========================================
    # CHALLENGE 3 — PRODUCT RULE
    # ==========================================

    elif st.session_state.room4_object == "lock3":

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">LOCK III — PRODUCT RULE WITH EXPONENTIAL AND TRIGONOMETRIC FUNCTIONS</div>',
                unsafe_allow_html=True
            )

            st.write("Find the derivative of the function:")

            st.latex(r"f(x) = e^x \tan x")

            answer = st.text_input(
                "YOUR ANSWER",
                key="r4_answer3"
            )

            left, right = st.columns(2)

            with left:

                if st.button(
                    "SUBMIT ANSWER",
                    key="r4_submit3",
                    type="primary",
                    use_container_width=True
                ):

                    normalized = (
                        answer.lower()
                        .replace(" ", "")
                        .replace("**", "^")
                        .replace("*", "")
                    )

                    is_correct = normalized in [
                        "e^xtan(x)+e^xsec^2(x)",
                        "e^x(sec^2(x)+tan(x))",
                        "e^xtanx+e^xsec^2x",
                        "e^x(sec^2x+tanx)"
                    ]

                    save_attempt(
                        "ROOM 4 - EXIT DOOR",
                        3,
                        "f(x) = e^x tan x",
                        answer,
                        "e^x tan(x)+e^x sec^2(x)",
                        is_correct
                    )

                    if is_correct:

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

                if st.button(
                    "USE HINT",
                    key="r4_hint3",
                    type="secondary",
                    use_container_width=True
                ):

                    if st.session_state.hint_used_this_question:

                        st.session_state.hint_message = (
                            "You can only use a hint once per challenge!"
                        )

                    else:

                        use_hint(
                            "Apply the Product Rule: (uv)' = u'v + uv'. Remember that the derivative of tan(x) is sec²(x)."
                        )

                    st.rerun()

    # ==========================================
    # FEEDBACK
    # ==========================================

    if st.session_state.feedback == "correct":

        st.success("Correct! You completed the lock.")

        if st.button(
            "CONTINUE",
            key="room4_continue",
            type="primary"
        ):

            completed_lock = st.session_state.room4_object

            if completed_lock not in st.session_state.room4_completed:
                st.session_state.room4_completed.append(completed_lock)

            st.session_state.notification = ""
            st.session_state.notification_type = ""

            st.session_state.feedback = ""
            st.session_state.hint_message = ""
            st.session_state.hint_used_this_question = False

            st.session_state.room4_object = None

            st.session_state.question_number = len(
                st.session_state.room4_completed
            )

            # ==================================
            # ALL THREE LOCKS COMPLETED
            # ==================================

            if len(st.session_state.room4_completed) == 3:

                st.session_state.room4_cleared = True
                st.session_state.end_time = time.time()

                if "Crystal Key" not in st.session_state.keys_collected:

                    st.session_state.keys_collected.append(
                        "Crystal Key"
                    )

                st.session_state.question_number = 0
                st.session_state.page = "ending"

            st.rerun()

    elif st.session_state.feedback == "wrong":

        st.error(
            "Incorrect! One life and five seconds deducted."
        )

        st.session_state.feedback = ""

        if st.session_state.game_over:
            st.rerun()

    # ==========================================
    # HINT MESSAGE
    # ==========================================

    if st.session_state.hint_message:

        st.info(st.session_state.hint_message)

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True
    )

# ==========================================
# ENDING PAGE
# ==========================================

def ending_page():

    design()

    st.write("")
    st.write("")

    # ENDING TITLE
    st.markdown("""
        <div class="section-title" style="text-align:center">
            THE FINAL MOMENT
        </div>

        <div class="main-title">
            YOU ESCAPED
        </div>

        <div class="subtitle">
            The Locked Classroom
        </div>

        <div class="gold-line"></div>
    """, unsafe_allow_html=True)

    st.write("")

    # ENDING STORY
    left, center, right = st.columns([1, 5, 1])

    with center:
        with st.container(border=True):

            st.markdown("""
                <div class="section-title" style="text-align:center">
                    ✦ THE EXIT IS OPEN ✦
                </div>
            """, unsafe_allow_html=True)

            st.write("")

            st.markdown("""
                <div class="story-text" style="text-align:center">
                    The classroom doors slowly swing open.
                    <br><br>
                    After solving every challenge and collecting
                    all four keys, you have finally found your way out.
                    <br><br>
                    The silence is broken.
                    The test is over.
                    <br><br>
                    <em>You have successfully escaped the classroom.</em>
                </div>
            """, unsafe_allow_html=True)

            st.write("")

            st.markdown("""
                <div class="subtitle" style="text-align:center">
                    4 ROOMS CLEARED • 12 CHALLENGES SOLVED
                </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # CONGRATULATIONS MESSAGE
    st.markdown("""
        <div class="section-title" style="text-align:center">
            CONGRATULATIONS, ESCAPE COMPLETE!
        </div>
    """, unsafe_allow_html=True)

    st.write("")

    # ACHIEVEMENTS AND REVIEW ANSWERS BUTTONS
    left, achievements, review, right = st.columns(
        [1, 2.5, 2.5, 1]
    )

    with achievements:
        if st.button(
            "🏆 SEE ACHIEVEMENTS",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "achievements"
            st.rerun()

    with review:
        if st.button(
            "📖 REVIEW ANSWERS",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "review"
            st.rerun()

    st.write("")
    st.write("")

    # ENDING BUTTONS
    left, again, gap, menu, right = st.columns(
        [1, 2.5, 0.3, 2.5, 1]
    )

    with again:
        if st.button(
            "PLAY AGAIN",
            type="secondary",
            use_container_width=True
        ):
            reset_game()
            st.session_state.page = "story"
            st.rerun()

    with menu:
        if st.button(
            "MAIN MENU",
            type="secondary",
            use_container_width=True
        ):
            reset_game()
            st.session_state.page = "home"
            st.rerun()

# ==========================================
# ACHIEVEMENTS PAGE
# ==========================================



def achievements_page():

    design()

    st.write("")
    st.write("")

    # PAGE TITLE
    st.markdown("""
        <div class="section-title" style="text-align:center">
            YOUR FINAL REWARDS
        </div>

        <div class="main-title">
            ACHIEVEMENTS
        </div>

        <div class="subtitle">
            The Locked Classroom
        </div>

        <div class="gold-line"></div>
    """, unsafe_allow_html=True)

    st.write("")

    # ACHIEVEMENT DATA
    achievements = [
        {
            "name": "KEY COLLECTOR",
            "icon": "🔑",
            "description": "Collect all four keys.",
            "unlocked": len(st.session_state.keys_collected) == 4
        },
        {
            "name": "UNTOUCHABLE",
            "icon": "❤️",
            "description": "Finish the game with all three lives.",
            "unlocked": st.session_state.lives == 3
        },
        {
            "name": "INDEPENDENT THINKER",
            "icon": "💡",
            "description": "Complete the game without using hints.",
            "unlocked": st.session_state.hints_used == 0
        },
        {
            "name": "PERFECT RUN",
            "icon": "🎯",
            "description": "Complete the game without incorrect answers.",
            "unlocked": st.session_state.wrong_answers == 0
        },
        {
            "name": "ESCAPE MASTER",
            "icon": "🎓",
            "description": "Complete all twelve challenges.",
            "unlocked": (
                st.session_state.room1_cleared
                and st.session_state.room2_cleared
                and st.session_state.room3_cleared
                and st.session_state.room4_cleared
            )
        }
    ]

    # UNLOCKED COUNT
    unlocked_count = sum(
        achievement["unlocked"]
        for achievement in achievements
    )

    st.markdown(f"""
        <div style="
            text-align:center;
            font-size:20px;
            font-weight:bold;
            margin:15px 0 25px 0;
            color:#D4AF37;
        ">
            {unlocked_count} / {len(achievements)} ACHIEVEMENTS UNLOCKED
        </div>
    """, unsafe_allow_html=True)

    # ACHIEVEMENT CARDS
    for i in range(0, len(achievements), 2):

        col1, col2 = st.columns(2)

        for col, achievement in zip(
            [col1, col2],
            achievements[i:i + 2]
        ):

            with col:

                if achievement["unlocked"]:
                    status = "✓ UNLOCKED"
                    border_color = "#D4AF37"
                    opacity = "1"
                else:
                    status = "🔒 LOCKED"
                    border_color = "#555555"
                    opacity = "0.55"

                card_html = f"""
                    <div style="
                        border:1px solid {border_color};
                        border-radius:12px;
                        padding:25px 15px;
                        margin-bottom:18px;
                        text-align:center;
                        background:rgba(0,0,0,0.55);
                        opacity:{opacity};
                        min-height:190px;
                        font-family:Arial, sans-serif;
                    ">
                        <div style="
                            font-size:42px;
                            margin-bottom:10px;
                        ">
                            {achievement["icon"]}
                        </div>

                        <div style="
                            font-size:19px;
                            font-weight:bold;
                            color:#D4AF37;
                            margin-bottom:10px;
                        ">
                            {achievement["name"]}
                        </div>

                        <div style="
                            font-size:14px;
                            color:#FFFFFF;
                            margin-bottom:15px;
                        ">
                            {achievement["description"]}
                        </div>

                        <div style="
                            font-size:12px;
                            font-weight:bold;
                            color:{border_color};
                        ">
                            {status}
                        </div>
                    </div>
                """

                st.html(card_html)

    st.write("")
    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True
    )

    # BACK TO ENDING BUTTON
    left, center, right = st.columns([1, 2, 1])

    with center:
        if st.button(
            "← BACK TO ENDING",
            use_container_width=True
        ):
            st.session_state.page = "ending"
            st.rerun()


def review_answers():

    design()

    header(
        "REVIEW",
        "ANSWER HISTORY",
        "Review your submitted answers"
    )

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    rooms = [
        {
            "name": "ROOM 1 - BLACKBOARD",
            "questions": [
                r"\lim_{x\to2}(3x+4)",
                r"\lim_{x\to2}\frac{x^2-4}{x-2}",
                r"\lim_{x\to1}\frac{x^2+3x-4}{x-1}"
            ]
        },
        {
            "name": "ROOM 2 - TEACHER'S DESK",
            "questions": [
                r"f(x)=4x^3",
                r"f(x)=5x^2-3x+7",
                r"f(x)=10x^4+9x^3+4x^2+x+67"
            ]
        },
        {
            "name": "ROOM 3 - LIBRARY",
            "questions": [
                r"f(x)=x^2(3x+1)",
                r"f(x)=\frac{x}{x+1}",
                r"f(x)=(2x+3)^4"
            ]
        },
        {
            "name": "ROOM 4 - EXIT DOOR",
            "questions": [
                r"f(x)=\sin(2x)",
                r"f(u)=5^u",
                r"f(x)=e^x\tan(x)"
            ]
        }
    ]

    for room_index, room in enumerate(rooms):

        st.markdown(f"### {room['name']}")

        for challenge_index, question in enumerate(room["questions"], start=1):

            attempts = [
                item for item in st.session_state.answer_history
                if item["room"] == room["name"]
                and item["challenge"] == challenge_index
            ]

            with st.expander(f"CHALLENGE {challenge_index}"):

                st.write("**Question:**")
                st.latex(question)

                if not attempts:

                    st.warning("Not Attempted")

                else:

                    for attempt_number, attempt in enumerate(attempts, start=1):

                        st.markdown(f"**Attempt {attempt_number}**")

                        st.write(f"Your Answer: {attempt['your_answer']}")

                        if attempt["is_correct"]:

                            st.success("Correct!")

                        else:

                            st.error("Incorrect!")
                            st.write(
                                f"Correct Answer: {attempt['correct_answer']}"
                            )

                        st.markdown("---")

        st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    if st.button("BACK TO ENDING", type="primary", use_container_width=True):

        st.session_state.page = "ending"
        st.rerun()

# ==========================================
# PAGE NAVIGATION
# ==========================================
presenter_mode()

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
    
elif st.session_state.page == "room4":
    room4()
    
elif st.session_state.page == "ending":
    ending_page()
    
elif st.session_state.page == "achievements":
    achievements_page()
    
elif st.session_state.page == "review":
    review_answers()
