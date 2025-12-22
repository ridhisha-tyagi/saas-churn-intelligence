import streamlit as st

def product_breakdown_view():
    st.title("🧩 Product Breakdown")

    st.markdown(
        "Deep-dive into **how product features impact churn, retention, and customer value**."
    )

    st.markdown("---")

    col1, col2, col3, col4 , col5 = st.columns(5)

    with col1:
        if st.button("📊 Feature Usage vs Churn", key="product_feature_usage"):
            st.session_state.view = "product_feature_usage"

    with col2:
        if st.button("❤️ Feature Health Matrix", key="product_feature_health"):
            st.session_state.view = "product_feature_health"
            
    with col3:
        if st.button("🔥 Churn Drivers", key="product_churn_drivers"):
            st.session_state.view = "product_churn_drivers"        

    with col4:
        if st.button("🛡 Retention Drivers", key="product_retention_drivers"):
            st.session_state.view = "product_retention_drivers"
            
    with col5:
        if st.button("🧩 Final Product Insights"):
            st.session_state.view = "product_final_insights"
        

    st.markdown("---")

    if st.button("⬅ Back to Home", key="back_from_product"):
        st.session_state.view = "home"
