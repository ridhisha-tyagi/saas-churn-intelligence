import streamlit as st

def behavior_analysis_view():
    st.title("🧠 Behavior Analysis")

    st.markdown("Explore how churned vs retained users behave over time.")

    col1, col2 , col3 , col4 , col5 = st.columns(5)

    with col1:
        if st.button("😊 Satisfaction", key="behavior_satisfaction"):
            st.session_state.view = "behavior_satisfaction"

    with col2:
        if st.button("📊 Usage", key="behavior_usage"):
            st.session_state.view = "behavior_usage"
            
    with col3:        
        if st.button("🎧 Support Behavior", key="support_behavior"):
            st.session_state.view = "behavior_support"

    with col4:
        if st.button("🚨 Errors", key="behavior_errors"):
            st.session_state.view = "behavior_errors"

    st.markdown("---")

    if st.button("⬅ Back to Analysis", key="back_to_analysis"):
        st.session_state.view = "analysis"
