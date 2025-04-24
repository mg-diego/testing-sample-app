import pandas as pd
import streamlit as st
import streamlit_antd_components as sac
from common.jwt_utils import verify_permission, verify_token
from common.permissions import Permissions

import requests

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENVIRONMENT = "DOCKER"

CATALOG_API_BASE_URL = "catalog-management" if ENVIRONMENT == "DOCKER" else "localhost"
USER_MANAGEMENT_API_BASE_URL = "user-management" if ENVIRONMENT == "DOCKER" else "localhost"

st.set_page_config(page_title="TESTING SAMPLE APP", layout="wide")
st.markdown("""
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #007ACC;
            color: #FFFFFF;
            text-align: center;
            padding: 5px;
            font-size: 14px;
            z-index: 999999;
            border-top: 1px solid #eaeaea;
        }
        a:link {
            color: white;
            background-color: transparent;
            text-decoration: none;
        }
        a:visited {
            color: pink;
            background-color: transparent;
            text-decoration: none;
        }
        a:hover {
            color: #CCCCCC;
            background-color: transparent;
            text-decoration: underline;
        }
        a:active {
            color: yellow;
            background-color: transparent;
            text-decoration: underline;
        }
        .stDataFrame table td {
            white-space: pre-wrap;  /* Permite los saltos de línea dentro de las celdas */
            word-wrap: break-word;  /* Se asegura de que las palabras largas se ajusten correctamente */
        }
    </style>

    <div class="footer">
        <a href="https://github.com/mg-diego/timeline-explorer" target="_blank"
                class="text-decoration-none d-inline-flex align-items-center">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub"
                    width="16" height="16" class="me-1" />
                 Testing Sample App - github.com/mg-diego
            </a>
    </div>
""", unsafe_allow_html=True)

def show_sidebar():

    menu_items = [sac.MenuItem('Homepage')]
    if verify_permission(Permissions.ACCESS_CATALOG_MANAGEMENT, st.session_state["access_token"]):
        menu_items.append(sac.MenuItem('Catalog', icon='bar-chart'))

    if verify_permission(Permissions.ACCESS_USER_MANAGEMENT, st.session_state["access_token"]):
        menu_items.append(sac.MenuItem('User Management', icon='line-chart'))

    menu_items.append(sac.MenuItem('Exit'))

    with st.sidebar:
        menu_id = sac.menu(
            items=menu_items,
            open_all=True,
            index=0,
        )
        
    if menu_id == "Homepage":
        st.header("TESTING SAMPLE APP - Homepage")

    if menu_id == "Catalog":
        st.header("TESTING SAMPLE APP - Catalog")

    if menu_id == "User Management":
        st.header("TESTING SAMPLE APP - User Management")

        tab1, tab2, tab3 = st.tabs(["List of Users", "Create User", "Delete User"])

        with tab1:
            if verify_permission(Permissions.READ_USERS, st.session_state["access_token"]):
                headers = {
                    "Authorization": "Bearer " + st.session_state["access_token"]
                }
                response = requests.get(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/users", headers=headers)

                df = pd.DataFrame(response.json())

                st.write("### Users Table")
                st.dataframe(df, use_container_width=True)
            else:
                st.write("The current user has no permission to read users.")

        with tab2:
            if verify_permission(Permissions.CREATE_USERS, st.session_state["access_token"]):
                st.write("The current user has permission to create users.")
            else:
                st.write("The current user has no permission to create users.")

        with tab3:
            if verify_permission(Permissions.DELETE_USERS, st.session_state["access_token"]):
                headers = {
                    "Authorization": "Bearer " + st.session_state["access_token"]
                }
                response = requests.get(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/users", headers=headers)

                df = pd.DataFrame(response.json())
                usernames = df["username"].tolist()
                selected_user = st.selectbox("Select a user", usernames)

                if st.button("Delete", type="primary"):
                    if selected_user == verify_token(st.session_state['access_token'])["username"]:
                        st.error("You can't delete your own user.", icon="⚠️")
                    else:
                        st.write(f"You deleted the user {selected_user}.")
            else:
                st.write("The current user has no permission to delete users.")

    if menu_id == "Exit":
        st.session_state.clear()
        st.rerun()
    

# Login
def login():
    col1, col2, col3 = st.columns(3)

    with col1, col3:
        pass

    with col2:
        st.header("TESTING SAMPLE APP")
        st.markdown(f'<small style="color: gray;">(Default user: admin / admin)</small>', unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            try:
                with st.spinner("Wait for it..."):
                    res = requests.post(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/login/?username={username}&password={password}")
                    if res.ok:
                        response_content = res.json()
                        st.session_state["access_token"] = response_content["access_token"]
                        st.rerun()
                                        
                    if res.status_code == 404:
                        st.error(res.json()["detail"], icon="⚠️")
            except Exception as e:
                st.error(e, icon="⚠️")

if "access_token" not in st.session_state:
    login()

if "access_token" in st.session_state:    
    show_sidebar()
