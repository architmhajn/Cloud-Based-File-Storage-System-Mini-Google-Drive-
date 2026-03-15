import streamlit as st
import os

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

st.title("☁ Mini Google Drive")

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

st.subheader("Stored Files")

files = os.listdir(UPLOAD_FOLDER)

for file in files:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(file)

    with col2:
        with open(os.path.join(UPLOAD_FOLDER, file), "rb") as f:
            st.download_button("Download", f, file_name=file)

    with col3:
        if st.button("Delete", key=file):
            os.remove(os.path.join(UPLOAD_FOLDER, file))
            st.rerun()