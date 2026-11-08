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
