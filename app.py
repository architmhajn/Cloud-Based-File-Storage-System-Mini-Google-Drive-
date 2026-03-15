import streamlit as st
import os

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

st.sidebar.title("📁 Dashboard")
st.sidebar.write("Mini Google Drive")
st.sidebar.write("Manage your files easily")

file_count = len(os.listdir(UPLOAD_FOLDER))
st.sidebar.metric("Total Files", file_count)

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

    file_path = os.path.join(UPLOAD_FOLDER, file)

    with col1:
        size = os.path.getsize(file_path) / 1024
        st.write(f"{file} ({size:.2f} KB)")

    with col2:
        if file.endswith(("png","jpg","jpeg")):
            st.image(file_path, width=150)

        with open(file_path, "rb") as f:
            st.download_button("Download", f, file_name=file)

    with col3:
        if st.button("Delete", key=file):
            os.remove(file_path)
            st.rerun()