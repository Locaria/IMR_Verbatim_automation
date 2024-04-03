import streamlit as st
import requests
import re
import tempfile
import shutil

# URL extract function
def extract_project_id(url):
    pattern = re.compile(r"/show/([A-Za-z0-9]+)")
    match = pattern.search(url)
    return match.group(1) if match else None
# Login function
def login(username, password):
    auth_url = "https://cloud.memsource.com/web/api2/v1/auth/login"
    credentials = {"userName": username, "password": password}
    response = requests.post(auth_url, json=credentials)
    return response.json().get("token") if response.status_code == 200 else None

# cosmetic CSS changes to the form
def apply_custom_styles():
    st.markdown("""
        <style>
        .reportview-container .main .block-container {
            max-width: 330px;
            padding-top: 5rem;
            margin: 0 auto;
        }
        .reportview-container .main {
            color: #000;
            background-color: #fff;
        }
        .block-container .markdown-text-container {
            padding-bottom: 0;
        }
        .stTextInput>div>div>input {
            margin-bottom: 0px;
        }
        .stButton>button {
            width: 100%;
            padding: 10px;
            margin-top: 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .info-text {
            font-size: 1em;
            margin-top: 10px;
            color: #666;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

# Login and CSS
def show_login_form():
    apply_custom_styles()  
    st.markdown("## Login")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    st.markdown("""
    <p class="info-text">REMEMBER - Enter your Phrase username, not your email.</p>
    """, unsafe_allow_html=True)
    if st.button("Login"):
        token = login(username, password)
        if token:
            st.session_state['access_token'] = token
            st.success("Logged in successfully.")
            st.experimental_rerun()
        else:
            st.error("Failed to login. Please check your credentials.")

def main():
    # If not  logged in, redirect to the login page
    if 'access_token' not in st.session_state:
        show_login_form()
    else:
        st.subheader("URL Page")
        user_url = st.text_input("Enter the project URL:")
        if st.button("Submit"):
            project_id = extract_project_id(user_url)
            if project_id:
                get_list_analyses_project = f"https://cloud.memsource.com/web/api2/v3/projects/{project_id}/analyses"
                headers = {"Authorization": f"ApiToken {st.session_state['access_token']}"}
                response = requests.get(get_list_analyses_project, headers=headers)
                if response.status_code == 200:
                    analyses = response.json().get("content")
                    analyseUid = analyses[0]['uid'] if analyses else None
                    if analyseUid:
                        download_analysis = f"https://cloud.memsource.com/web/api2/v1/analyses/{analyseUid}/download?format=csv"
                        response = requests.get(download_analysis, headers=headers, stream=True)
                        if response.status_code == 200:
                            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                                shutil.copyfileobj(response.raw, tmp_file)
                                st.success("Analysis downloaded successfully.")
                                st.download_button(label="Download Analysis CSV", data=tmp_file.name, file_name="analysis.csv")
                        else:
                            st.error("Failed to download analysis.")
                    else:
                        st.error("AnalyseUid not found.")
                else:
                    st.error("Failed to retrieve project information.")
            else:
                st.error("Project ID not found in URL.")

if __name__ == "__main__":
    main()
