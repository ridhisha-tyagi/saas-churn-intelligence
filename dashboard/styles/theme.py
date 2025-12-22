import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* HERO BACKDROP */
.hero-glow {
    position: absolute;
    top: 5vh;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;          /* ↓ was 720 */
    height: 800px;         /* ↓ was 280 */
    background: linear-gradient(
        180deg,
        rgba(168, 85, 247, 0.22),
        rgba(168, 85, 247, 0.06)
    );
    border-radius: 28px;
    z-index: 0;

}

    /* Hide Streamlit chrome */
    [data-testid="stHeader"] {
        display: none;
    }

    [data-testid="stFooter"] {
        display: none;
    }

    /* App background */
    .stApp {
        background: radial-gradient(
            circle at top,
            #2a1458 0%,
            #160b2e 40%,
            #0b0616 75%
        );
        color: #f5f3ff;
    }

    /* Default padding */
    .block-container {
        padding-top: 2rem;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        height: 4rem;
        font-size: 2.15rem;
        font-weight: 600;
        background: linear-gradient(135deg, #A855F7, #C084FC);
        color: #0b0616;
        border-radius: 18px;
        border: none;
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.35);
        transition: all 0.25s ease-in-out;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        background: linear-gradient(135deg, #C084FC, #E9D5FF);
        box-shadow: 0 14px 40px rgba(168, 85, 247, 0.55);
    }

    /* Expanders */
    .st-expander {
        background-color: #1B1234;
        border-radius: 14px;
        border: 1px solid #31225C;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background-color: #1B1234;
        border-radius: 14px;
        padding: 1rem;
        border: 1px solid #31225C;
    }

    /* Titles */
    h1, h2, h3 {
        color: #E9D5FF;
    }

    </style>
    """, unsafe_allow_html=True)
