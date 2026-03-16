import streamlit as st
import os
import json

USERS_FILE = "users.json"
UPLOAD_FOLDER = "uploads"

# Create folders/files if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)


def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


st.title("☁ Mini Cloud File Sharing")

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Signup", "View Profiles"]
)

users = load_users()

# ---------------- SIGNUP ----------------

if menu == "Signup":

    st.header("Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Create Account"):

        if new_user in users:
            st.error("Username already exists")

        else:
            users[new_user] = new_pass
            save_users(users)

            os.makedirs(os.path.join(UPLOAD_FOLDER, new_user), exist_ok=True)

            st.success("Account created successfully!")

# ---------------- LOGIN ----------------

elif menu == "Login":

    st.header("Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if user in users and users[user] == password:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success("Logged in successfully")

        else:
            st.error("Invalid credentials")

# ---------------- VIEW PROFILES ----------------

elif menu == "View Profiles":

    st.header("User Profiles")

    profile = st.text_input("Enter username to view profile")

    if profile:

        profile_folder = os.path.join(UPLOAD_FOLDER, profile)

        if os.path.exists(profile_folder):

            st.subheader(f"{profile}'s Files")

            files = os.listdir(profile_folder)

            for file in files:

                file_path = os.path.join(profile_folder, file)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(file)

                with col2:
                    with open(file_path, "rb") as f:
                        st.download_button("Download", f, file_name=file)

                with col3:
                    if st.session_state.logged_in and st.session_state.username == profile:
                        if st.button("Delete", key=file):
                            os.remove(file_path)
                            st.rerun()

        else:
            st.error("User not found")

# ---------------- USER DASHBOARD ----------------

if st.session_state.logged_in:

    st.sidebar.write(f"Logged in as **{st.session_state.username}**")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.header("Upload Files")

    uploaded_files = st.file_uploader(
        "Upload files",
        accept_multiple_files=True
    )

    if uploaded_files:

        user_folder = os.path.join(UPLOAD_FOLDER, st.session_state.username)

        for uploaded_file in uploaded_files:

            file_path = os.path.join(user_folder, uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"{uploaded_file.name} uploaded!")