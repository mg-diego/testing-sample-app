import pandas as pd
import streamlit as st
import streamlit_antd_components as sac
from common.jwt_utils import verify_permission
from common.permissions import Permissions
from translations_service import get_translation, update_translations

import requests

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENVIRONMENT = "local"
WEB_TITLE = "🕵️ TESTING SAMPLE APP"

CATALOG_API_BASE_URL = "catalog-management" if ENVIRONMENT == "DOCKER" else "localhost"
USER_MANAGEMENT_API_BASE_URL = "user-management" if ENVIRONMENT == "DOCKER" else "localhost"
LANGUAGE_MANAGEMENT_API_BASE_URL = "language-management" if ENVIRONMENT == "DOCKER" else "localhost"

def get_headers():
    return  { "Authorization": "Bearer " + st.session_state["access_token"] }

def show_toast(response: requests.Response, custom_message):
    response_json = response.json()
    if response.ok:
        st.session_state.toast['text'] = f"{custom_message}"
        st.session_state.toast['icon'] = "✅"
    else:
        st.session_state.toast['text'] = get_translation(f"errors.{response_json['detail']}")
        st.session_state.toast['icon'] = "🚨"

st.set_page_config(page_title=WEB_TITLE, layout="wide")
st.markdown("""
    <style>    
            /* Tab container background */
        div[data-testid="stTabs"] > div {
            border-radius: 5px;
            padding: 10px;
        }

        /* Active tab label */
        button[data-baseweb="tab"] {
            background-color: #e0e0e0;
            border-radius: 5px 5px 0 0;
            padding: 10px;
            margin-right: 5px;
        }

        /* Hover effect */
        button[data-baseweb="tab"]:hover {
            background-color: #d0d0d0;
        }

        /* Selected tab label */
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #c0c0c0;
            font-weight: bold;
        }   
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

@st.dialog("New Catalog")
def create_catalog():
    st.write(f"New Catalog")
    name = st.text_input("Name", placeholder="Name")
    description = st.text_input("Description", placeholder="Description")
    if st.button("Create"):
        body = {
            "name": name,
            "description": description
        }
        response = requests.post(f"http://{CATALOG_API_BASE_URL}:8002/catalog/", headers=get_headers(), json=body)
        show_toast(response, get_translation('catalog.toast.create') % name)
        st.rerun()

@st.dialog("Delete Catalog?")
def delete_catalog(catalog_id, catalog_name, catalog_description):
    st.write("Confirm that you want to delete this catalog.")
    st.text_input("Name", value=catalog_name, disabled=True)
    st.text_input("Description", value=catalog_description, disabled=True)
    st.caption(f"ID: {catalog_id}")
    if st.button("Delete"):
        response = requests.delete(f"http://{CATALOG_API_BASE_URL}:8002/catalog/?catalog_id={catalog_id}", headers=get_headers())
        show_toast(response, get_translation('catalog.toast.delete') % catalog_id)
        st.rerun()

@st.dialog("Edit Catalog")
def edit_catalog(catalog_id, catalog_name, catalog_description):
    name = st.text_input("Name", value=catalog_name)
    description = st.text_input("Description", value=catalog_description)
    st.caption(f"ID: {catalog_id}")
    if st.button("Save changes"):
        body = {
            "_id": catalog_id,
            "name": name,
            "description": description
        }
        response = requests.put(f"http://{CATALOG_API_BASE_URL}:8002/catalog/", headers=get_headers(), json=body)
        show_toast(response, get_translation('catalog.toast.edit') % catalog_id)
        st.rerun()

@st.dialog("Catalog Details")
def details_catalog(catalog_id, catalog_name, catalog_description):
    st.text_input("Name", value=catalog_name, disabled=True)
    st.text_input("Description", value=catalog_description, disabled=True)
    st.caption(f"ID: {catalog_id}")
    if st.button("Close"):
        st.rerun()

def show_web():
    homepage_tab, catalog_tab, user_management_tab, language_tab, logout_tab = st.tabs([
            "Homepage",
            "Catalog",
            "User Management",
            "Language",
            "Logout"
    ])

    with homepage_tab:
        st.header(f"{WEB_TITLE} - {get_translation('menu.homepage')}")

        st.markdown(f"""
            <h2>{get_translation('homepage.header')} Testing Sample App!</h2>
            <p>{get_translation('homepage.paragraph1')}</p>
            <ul>
                <li><strong>{get_translation('homepage.feature1.name')}</strong>: {get_translation('homepage.feature1.description')}</li>
                <li><strong>{get_translation('homepage.feature2.name')}</strong>: {get_translation('homepage.feature2.description')}</li>
                <li><strong>{get_translation('homepage.feature3.name')}</strong>: {get_translation('homepage.feature2.description')}</li>
                <li><strong>{get_translation('homepage.feature4.name')}</strong>: {get_translation('homepage.feature2.description')}</li>
            </ul>
            <p>{get_translation('homepage.paragraph2')}</p>
        """, unsafe_allow_html=True)

    with catalog_tab:
        st.header(f"{WEB_TITLE} - {get_translation('menu.catalog')}")
        first_search = True

        search_value = st.text_input(label=get_translation('catalog.filter.label'), placeholder=get_translation('catalog.filter.placeholder'))
        create_btn = st.button('Create New', type="primary")            

        if search_value or first_search:
            response = (requests.get(f"http://{CATALOG_API_BASE_URL}:8002/catalog/?filter={search_value}", headers=get_headers()).json())
            cols = st.columns(4)

            for i, item in enumerate(response['detail']):
                with cols[i % 4]:
                    with st.form(key=f"catalog-{item['_id']}"):
                        st.markdown(f"### {item['name']}")
                        st.write(item['description'])
                        st.caption(f"ID: {item['_id']}")

                        details_button = st.form_submit_button(f"📜 {get_translation('catalog.button.details')}")
                        if details_button:
                            details_catalog(item['_id'], item['name'], item['description'])

                        if verify_permission(Permissions.UPDATE_CATALOG, st.session_state["access_token"]):
                            edit_button = st.form_submit_button(f"✏️ {get_translation('catalog.button.edit')}")
                            if edit_button:
                                edit_catalog(item['_id'], item['name'], item['description'])

                        if verify_permission(Permissions.DELETE_CATALOG, st.session_state["access_token"]):
                            delete_button = st.form_submit_button(f"🗑️ {get_translation('catalog.button.delete')}")
                            if delete_button:
                                delete_catalog(item['_id'], item['name'], item['description'])                                    

        if create_btn:
            create_catalog()

    with user_management_tab:
        st.header(f"{WEB_TITLE} - {get_translation('menu.userManagement')}")

        tab1, tab2, tab3 = st.tabs([
            get_translation("userManagement.tab.listOfUsers"),
            get_translation("userManagement.tab.createUser"),
            get_translation("userManagement.tab.deleteUser")
        ])

        with tab1:
            if verify_permission(Permissions.READ_USERS, st.session_state["access_token"]):
                list_of_users_response = requests.get(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/users", headers=get_headers())
                list_of_users_response_json = list_of_users_response.json()

                if list_of_users_response.ok:
                    df = pd.DataFrame(list_of_users_response_json['detail'])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error(list_of_users_response_json['detail'])

            else:
                st.write(get_translation("userManagement.listOfUsers.noPermission"))

        with tab2:
            if verify_permission(Permissions.CREATE_USERS, st.session_state["access_token"]):
                with st.form("user_form", clear_on_submit=True):
                    st.subheader(get_translation("userManagement.createUser.subheader"))

                    username = st.text_input(get_translation("login.username"))
                    password = st.text_input(get_translation("login.password"), type="password")
                    repeat_password = st.text_input(get_translation("userManagement.createUser.form.repeatPassword"), type="password")

                    st.markdown(f"### {get_translation('userManagement.createUser.form.permissions')}")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        access_catalog_permission = st.checkbox(Permissions.ACCESS_CATALOG_MANAGEMENT.name, help=get_translation("userManagement.createUser.form.accessCatalog.info"))
                        access_user_management_permission = st.checkbox(Permissions.ACCESS_USER_MANAGEMENT.name, help=get_translation('userManagement.createUser.form.accessUserManagement.info'))
                        set_language_permission = st.checkbox(Permissions.SET_LANGUAGE.name, help=get_translation("userManagement.createUser.form.setLanguage.info"))

                    with col2:
                        edit_catalog_permission = st.checkbox(Permissions.UPDATE_CATALOG.name, help=get_translation('userManagement.createUser.form.editCatalog.info'))
                        create_catalog_permission = st.checkbox(Permissions.CREATE_CATALOG.name, help=get_translation('userManagement.createUser.form.createCatalog.info'))
                        delete_catalog_permission = st.checkbox(Permissions.DELETE_CATALOG.name, help=get_translation('userManagement.createUser.form.deleteCatalog.info'))

                    with col3:
                        read_users_permission = st.checkbox(Permissions.READ_USERS.name, help=get_translation("userManagement.createUser.form.readUsers.info"))
                        create_users_permission = st.checkbox(Permissions.CREATE_USERS.name, help=get_translation("userManagement.createUser.form.createUsers.info"))
                        delete_users_permission = st.checkbox(Permissions.DELETE_USERS.name, help=get_translation("userManagement.createUser.form.deleteUsers.info"))

                    # Submit button
                    submitted = st.form_submit_button(get_translation("userManagement.createUser.form.submitButton"))

                    if submitted:
                        error_message = ""
                        permissions = [
                            access_catalog_permission,
                            access_user_management_permission,
                            create_catalog_permission,
                            edit_catalog_permission,
                            delete_catalog_permission,
                            set_language_permission,
                            read_users_permission,
                            create_users_permission,
                            delete_users_permission
                        ]

                        if username == "":
                            error_message += f"\n - {get_translation('userManagement.createUser.form.errors.usernameEmpty')}"
                        if password == "":
                            error_message += f"\n - {get_translation('userManagement.createUser.form.errors.passwordEmpty')}"
                        if repeat_password == "":
                            error_message += f"\n - {get_translation('userManagement.createUser.form.errors.repeatPasswordEmpty')}"
                        if password != repeat_password:
                            error_message += f"\n - {get_translation('userManagement.createUser.form.errors.passwordsDontMatch')}"
                        if not any(permissions):
                            error_message += f"\n - {get_translation('userManagement.createUser.form.errors.noPermissions')}"

                        if error_message != "":
                            st.error(f"{get_translation('userManagement.createUser.form.errors')} {error_message}", icon="⚠️")                            

                        else:
                            permissions = []
                            if access_catalog_permission:
                                permissions.append(Permissions.ACCESS_CATALOG_MANAGEMENT.name)
                            if access_user_management_permission:
                                permissions.append(Permissions.ACCESS_USER_MANAGEMENT.name)
                            if create_catalog_permission:
                                permissions.append(Permissions.CREATE_CATALOG.name)
                            if edit_catalog_permission:
                                permissions.append(Permissions.UPDATE_CATALOG)
                            if delete_catalog_permission:
                                permissions.append(Permissions.DELETE_CATALOG)
                            if read_users_permission:
                                permissions.append(Permissions.READ_USERS.name)
                            if create_users_permission:
                                permissions.append(Permissions.CREATE_USERS.name)
                            if delete_users_permission:
                                permissions.append(Permissions.DELETE_USERS.name)
                            if set_language_permission:
                                permissions.append(Permissions.SET_LANGUAGE.name)

                            body = {
                                "username": username,
                                "password": password,
                                "permissions": permissions
                            }
                            create_response = requests.post(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/users", headers=get_headers(), json=body)
                            show_toast(create_response, get_translation('userManagement.createUser.toast.success') % username)
                            st.rerun()

            else:
                st.write(get_translation('userManagement.createUser.noPermission'))

        with tab3:
            if verify_permission(Permissions.DELETE_USERS, st.session_state["access_token"]):
                df = pd.DataFrame(list_of_users_response_json['detail'])
                usernames = df["username"].tolist()
                selected_user = st.selectbox(get_translation('userManagement.deleteUser.selectUser'), usernames)

                if st.button(get_translation('userManagement.deleteUser.deleteButton'), type="primary"):
                    delete_response = requests.delete(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/users", headers=get_headers(), params={"username": selected_user})
                    show_toast(delete_response, get_translation('userManagement.deleteUser.toast.success') % selected_user)
                    st.rerun()
                        
            else:
                st.write(get_translation("userManagement.deleteUser.noPermission"))

    with language_tab:
        st.header(f"{WEB_TITLE} - {get_translation('menu.language')}")

        with st.form("Select language"):
            st.subheader(get_translation("language.form.header"))
            languages_response = requests.get(f"http://{LANGUAGE_MANAGEMENT_API_BASE_URL}:8003/language", headers=get_headers())
            print(languages_response)
            active_language = languages_response.json()['detail']

            def get_language_code(language_name, languages):
                for language in languages:
                    if language[0] == language_name:
                        return str(language[1])
                    
            def get_language_index_by_code(code: str, languages: list) -> int:
                for index, (_, lang_code) in enumerate(languages):
                    if lang_code in code:
                        return index
                return -1  # Return -1 if not found          

            languages = [
                (f"🇺🇸 {get_translation('language.form.english')}", "en"),
                (f"🇪🇸 {get_translation('language.form.spanish')}", "es"),
                (f"🇫🇷 {get_translation('language.form.french')}", "fr"),
                (f"🇵🇹 {get_translation('language.form.portuguese')}", "pt"),
                (f"🇯🇵 {get_translation('language.form.japanese')}", "jp")
            ]
                            
            selected_language = st.radio(
                "",
                options=[lang[0] for lang in languages],
                index=get_language_index_by_code(active_language, languages)
            )

            # Submit button
            submitted = st.form_submit_button(get_translation("language.form.submitButton"))

            if submitted:                
                response = requests.post(f"http://{LANGUAGE_MANAGEMENT_API_BASE_URL}:8003/language/?language={get_language_code(selected_language, languages)}", headers=get_headers())
                if response.ok:
                    update_translations(requests.get(f"http://{LANGUAGE_MANAGEMENT_API_BASE_URL}:8003/language/translations").json())

                show_toast(response, get_translation("language.toast.success") % get_language_code(selected_language, languages).upper())
                st.rerun()

    with logout_tab:
       st.header(f"{WEB_TITLE} - {get_translation('menu.logout')}")
       logout_button = st.button(get_translation('menu.logout'), key="primary")
       if logout_button:
        st.session_state.clear()
        st.rerun()

def login():
    col1, col2, col3 = st.columns(3)

    with col1, col3:
        pass

    with col2:
        st.header("🕵️ TESTING SAMPLE APP")
        st.markdown(f'<small style="color: gray;">({get_translation("login.defaultUser")} admin / admin)</small>', unsafe_allow_html=True)

        username = st.text_input(get_translation('login.username'))
        password = st.text_input(get_translation('login.password'), type="password")
        
        if st.button(get_translation("login.loginButton"), type="primary"):
            try:
                with st.spinner(get_translation("login.spinnerWait")):
                    res = requests.post(f"http://{USER_MANAGEMENT_API_BASE_URL}:8001/login/?username={username}&password={password}")
                    response_content_detail = res.json()["detail"]
                    if res.ok:                        
                        st.session_state["access_token"] = response_content_detail["access_token"]
                        st.rerun()                                        
                    else:
                        st.error(get_translation(f"errors.{response_content_detail}"), icon="⚠️")

            except Exception as e:
                st.error(e, icon="⚠️")

if "access_token" not in st.session_state:
    update_translations(requests.get(f"http://{LANGUAGE_MANAGEMENT_API_BASE_URL}:8003/language/translations").json())
    login()

if "access_token" in st.session_state:    
    show_web()

if "toast" not in st.session_state:
    st.session_state['toast'] = {}

if st.session_state.toast != {}:
    text = st.session_state.toast['text']
    icon = st.session_state.toast['icon']
    st.session_state['toast'] = {}
    st.toast(icon=icon, body=text)
