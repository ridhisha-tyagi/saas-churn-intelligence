import streamlit as st

def analysis_view():
    st.title("📊 Analysis")

    st.markdown("Choose what you want to explore:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Feature Analysis", key="go_feature_analysis"):
            st.session_state.view = "feature_analysis"

    with col2:
        if st.button("🧠 Behavior Analysis"):
            st.session_state.view = "behavior_analysis"
    
    with col3:
        if st.button("🏭 Industry Analysis", key="industry_analysis"):
            st.session_state.view = "industry_analysis"



    st.divider()

    if st.button("⬅ Back to Home", key="back_home_from_analysis"):
        st.session_state.view = "home"
