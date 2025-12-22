import streamlit as st
import streamlit as st

from views.industry_heatmap import industry_heatmap_view
from views.industry_reason import industry_reason_view
from views.industry_feedback import industry_feedback_view

def industry_analysis_view():
    st.title("🏭 Industry Churn Analysis")

    st.markdown(
        "Understand **which industries churn**, **why they churn**, "
        "and **what users say before leaving**."
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📉 Industry Churn Heatmap", key="industry_heatmap"):
            st.session_state.industry_view = "heatmap"

    with col2:
        if st.button("🎯 Industry × Reason Codes", key="industry_reason"):
            st.session_state.industry_view = "reason"

    with col3:
        if st.button("💬 Industry Feedback Insights", key="industry_feedback"):
            st.session_state.industry_view = "feedback"

    st.markdown("---")

    if "industry_view" not in st.session_state:
        st.session_state.industry_view = None

    if st.session_state.industry_view is None:
        st.info("⬆ Select a section to explore industry churn.")


    if st.session_state.industry_view == "heatmap":
        industry_heatmap_view()

    elif st.session_state.industry_view == "reason":
        industry_reason_view()

    elif st.session_state.industry_view == "feedback":
        industry_feedback_view()

    # ---------- BACK ----------
    st.markdown("---")
    if st.button("⬅ Back to Analysis", key="back_from_industry"):
        st.session_state.view = "analysis"
        st.session_state.industry_view = None
