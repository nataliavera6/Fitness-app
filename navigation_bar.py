import streamlit as st

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "Community"

# --- Navigation bar ---
def navigation():
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "Home"
    with col2:
        if st.button("👥 Community"):
            st.session_state.page = "Community"
    with col3:
        if st.button("✔️ Activity"):
            st.session_state.page = "Activity"
    with col4:
        if st.button("🗡️ Challenges"):
            st.session_state.page = "Challenges"
    with col5:
        if st.button("🧭 Habits"):
            st.session_state.page = "Habit Tracker"
    st.markdown("---")
