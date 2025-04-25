import pandas as pd
import streamlit as st
import streamlit_antd_components as sac
from streamlit_card import card
from common.jwt_utils import verify_permission, verify_token
from common.permissions import Permissions

import requests

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENVIRONMENT = "DOCKER"
WEB_TITLE = "🕵️ TESTING SAMPLE APP"

CATALOG_API_BASE_URL = "catalog-management" if ENVIRONMENT == "DOCKER" else "localhost"
USER_MANAGEMENT_API_BASE_URL = "user-management" if ENVIRONMENT == "DOCKER" else "localhost"

st.set_page_config(page_title=WEB_TITLE, layout="wide")
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
        <a href="https://github.com/mg-diego/testing-sample-app" target="_blank"
                class="text-decoration-none d-inline-flex align-items-center">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub"
                    width="16" height="16" class="me-1" />
                 Testing Sample App - github.com/mg-diego
            </a>
    </div>
""", unsafe_allow_html=True)

def show_web():
    menu_items = [sac.MenuItem('Homepage')]
    if verify_permission(Permissions.ACCESS_CATALOG_MANAGEMENT, st.session_state["access_token"]):
        menu_items.append(sac.MenuItem('Catalog'))

    if verify_permission(Permissions.ACCESS_USER_MANAGEMENT, st.session_state["access_token"]):
        menu_items.append(sac.MenuItem('User Management'))

    menu_items.append(sac.MenuItem('Language'))
    menu_items.append(sac.MenuItem('Exit'))

    with st.sidebar:
        menu_id = sac.menu(
            items=menu_items,
            open_all=True,
            index=0,
        )
        
    if menu_id == "Homepage":
        st.header(f"{WEB_TITLE} - Homepage")

        st.markdown("""
            <h2>Welcome to the Testing App!</h2>
            <p>This application allows you to test and interact with various functionalities seamlessly. Below is an overview of the features:</p>
            <ul>
                <li><strong>User Management</strong>: Manage users, view user lists, and create new users with different permissions.</li>
                <li><strong>Language Selector</strong>: Choose your preferred language (English, Español, Français, etc.) to customize your experience.</li>
                <li><strong>Testing API Endpoints</strong>: Test API calls and interact with dynamic data.</li>
                <li><strong>Real-time Data</strong>: View real-time information from integrated services and APIs.</li>
            </ul>
            <p>Whether you're verifying user roles or experimenting with our services, this app provides a straightforward interface to perform and visualize testing tasks.</p>
        """, unsafe_allow_html=True)
        

    if menu_id == "Catalog":
        st.header(f"{WEB_TITLE} - (WIP) Catalog")

        filter_col1, filter_col2 = st.columns([1, 1])
        with filter_col1:            
            st.text_input(label="Filter:", placeholder="Filter by specific value...")
            st.button("Filter", type="primary")

        col1, col2, col3 = st.columns(3)

        with col1:
            card(
                title="Hello World!",
                text="Some description",
                image="https://placecats.com/100/200",
                url="https://github.com/gamcoh/st-card"
            )

        with col2:
            card(
                title="Hello World!",
                text="Some description",
                image="https://placecats.com/200/200",
                url="https://github.com/gamcoh/st-card"
            )

        with col3:
            card(
                title="Hello World!",
                text="Some description",
                image="https://placecats.com/300/200",
                url="https://github.com/gamcoh/st-card"
            )

    if menu_id == "User Management":
        st.header(f"{WEB_TITLE} - User Management")
        refresh_button = st.button("Refresh Data")

        if refresh_button:
            st.experimental_rerun()

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
                with st.form("user_form", clear_on_submit=True):
                    st.subheader("Create User")

                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    repeat_password = st.text_input("Repeat Password", type="password")

                    st.markdown("### Permissions")
                    col1, col2 = st.columns(2)

                    with col1:
                        access_catalog_permission = st.checkbox(Permissions.ACCESS_CATALOG_MANAGEMENT.name, help="Allows to navigate to the 'Catalog' menu")
                        access_user_management_permission = st.checkbox(Permissions.ACCESS_USER_MANAGEMENT.name, help="Allows to navigate to the 'User Management' menu")
                        create_catalog_permission = st.checkbox(Permissions.CREATE_CATALOG.name, help="Allows to create a new catalog.")

                    with col2:
                        read_users_permission = st.checkbox(Permissions.READ_USERS.name, help="Allows to read the list of users.")
                        create_users_permission = st.checkbox(Permissions.CREATE_USERS.name, help="Allows to create a new user.")
                        delete_users_permission = st.checkbox(Permissions.DELETE_USERS.name, help="Allows to delete an existing user.")

                    # Submit button
                    submitted = st.form_submit_button("Submit")

                    if submitted:
                        error_message = ""
                        permissions = [
                            access_catalog_permission,
                            access_user_management_permission,
                            create_catalog_permission,
                            read_users_permission,
                            create_users_permission,
                            delete_users_permission
                        ]

                        if username == "":
                            error_message += "\n - Username can't be empty."
                        if password == "":
                            error_message += "\n - Password can't be empty."
                        if repeat_password == "":
                            error_message += "\n - Repeat Password can't be empty."
                        if password != repeat_password:
                            error_message += "\n - Passwords do not match."
                        if not any(permissions):
                            error_message += "\n - At least one permission should be assigned."

                        if error_message != "":
                            st.error(f"Please fix the following errors: {error_message}", icon="⚠️")                            

                        else:
                            permissions = []
                            if access_catalog_permission:
                                permissions.append(Permissions.ACCESS_CATALOG_MANAGEMENT.name)
                            if access_user_management_permission:
                                permissions.append(Permissions.ACCESS_USER_MANAGEMENT.name)
                            if create_catalog_permission:
                                permissions.append(Permissions.CREATE_CATALOG.name)
                            if read_users_permission:
                                permissions.append(Permissions.READ_USERS.name)
                            if create_users_permission:
                                permissions.append(Permissions.CREATE_USERS.name)
                            if delete_users_permission:
                                permissions.append(Permissions.DELETE_USERS.name)

                            headers = {
                                "Authorization": "Bearer " + st.session_state["access_token"]
                            }
                            body = {
                                "username": username,
                                "password": password,
                                "permissions": permissions
                            }
                            response = requests.post(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/users", headers=headers, json=body)

                            if response.ok:
                                st.success(f"User '{username}' created successfully!")

                            else:
                                st.error(response.content, icon="⚠️")

            else:
                st.write("The current user has no permission to create users.")

        with tab3:
            if verify_permission(Permissions.DELETE_USERS, st.session_state["access_token"]):
                headers = {
                    "Authorization": "Bearer " + st.session_state["access_token"]
                }

                df = pd.DataFrame(response.json())
                usernames = df["username"].tolist()
                selected_user = st.selectbox("Select a user", usernames)

                if st.button("Delete", type="primary"):
                    if selected_user == verify_token(st.session_state['access_token'])["username"]:
                        st.warning("You can't delete your own user.", icon="⚠️")
                    else:
                        response = requests.delete(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/users", headers=headers, params={"username": selected_user})
                        
                        if response.ok:
                            st.success(f"User '{selected_user}' deleted successfully!")

                        else:
                            st.error(response.content, icon="⚠️")
            else:
                st.write("The current user has no permission to delete users.")

    if menu_id == "Language":
        st.header(f"{WEB_TITLE} - (WIP) Language")

        with st.form("Select language"):
            st.subheader("(WIP) Select Language")

            languages = [
                ("🇬🇧 English", "gb"),
                ("🇪🇸 Español", "es"),
                ("🇫🇷 Français", "fr"),
                ("🇵🇹 Português", "pt"),
                ("🇯🇵 Japonés", "jp")
            ]
                            
            selected_language = st.radio(
                "",
                options=[lang[0] for lang in languages],  # Flags as options
                index=0  # Default selected item (if you want to pre-select one)
            )

            # Submit button
            submitted = st.form_submit_button("Submit")

            if submitted:
                st.success(f"You selected: {selected_language}")


    if menu_id == "Exit":
        st.session_state.clear()
        st.rerun()
    

def login():
    col1, col2, col3 = st.columns(3)

    with col1, col3:
        pass

    with col2:
        st.header("🕵️ TESTING SAMPLE APP")
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
    show_web()
