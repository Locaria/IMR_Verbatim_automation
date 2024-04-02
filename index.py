import streamlit as st

st.set_page_config(page_title="Download Analysis", page_icon="📥")

with st.container():
    st.write("## Enter the project URL:")

    url = st.text_input("", placeholder="Paste the project URL here", help="Paste the project URL to be analyzed")
    if st.button("Download"):
        if url:
            st.success(f"URL submitted: {url}")
        else:
            st.error("Please enter a valid URL")