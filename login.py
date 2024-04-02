import streamlit as st

st.set_page_config(page_title="Login", page_icon=":key:")

with st.container():
    st.write("## Login")

    username = st.text_input("Username", placeholder="Username")
    password = st.text_input("Password", placeholder="Password", type="password")

    # Login  Button
    if st.button("Login"):
        if username == "admin" and password == "admin": 
            st.success("Logged in successfully!")
        else:
            st.error("Username or password is incorrect")

    st.write("REMEMBER - Enter Phrase username, the one you find in your Phrase profile, not your email.")