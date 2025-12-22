import streamlit as st

def home_view():

    # Spacer to align hero vertically
    st.markdown("<div style='height: 9vh'></div>", unsafe_allow_html=True)

    # HERO GLOW (background)
    st.markdown("""
    <div class="hero-glow"></div>
    """, unsafe_allow_html=True)

    # Centered content
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style="
            position: relative;
            z-index: 2;
            text-align: center;
            padding: 2rem 1rem;
        ">
        """, unsafe_allow_html=True)

        # TITLE
        st.markdown("""
        <h1 style="
            font-size: 5rem;
            font-weight: 800;
            margin-bottom: 0.6rem;
            color: #F5F3FF;
        ">
        🧠 SaaS Churn Intelligence
        </h1>

        <p style="
            font-size: 1.2rem;
            color: #c4b5fd;
            margin-bottom: 2.8rem;
        ">
        Churn analysis, product insights, and risk prioritization
        </p>
        """, unsafe_allow_html=True)

        # BUTTONS
        if st.button("📊 Product Breakdown"):
            st.session_state.view = "product_breakdown"

        st.markdown("<div style='height: 0.9rem'></div>", unsafe_allow_html=True)

        if st.button("🧠 Analysis"):
            st.session_state.view = "analysis"

        st.markdown("<div style='height: 0.9rem'></div>", unsafe_allow_html=True)

        if st.button("🔮 Churn Risk Prediction"):
            st.session_state.view = "churn_prediction"

        st.markdown("</div>", unsafe_allow_html=True)
