import streamlit as st

users = {
    "admin": {"password": "masterpass", "role": "Admin"},
    "adjutant": {"password": "admin123", "role": "Adjutant"},
    "s1": {"password": "s1pass", "role": "S1"},
    "finance": {"password": "finpass", "role": "Finance"},
    "commander": {"password": "viewonly", "role": "Command"}
}

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:

        st.title("🛡️ Integrated Longevity Audit System")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if username in users and users[username]["password"] == password:

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = users[username]["role"]

                st.success("Login successful")
                st.rerun()

            else:

                st.error("Invalid credentials")

        st.stop()
