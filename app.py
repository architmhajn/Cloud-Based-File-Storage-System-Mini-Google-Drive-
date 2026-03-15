import streamlit as st
import os

# Folder to store uploaded files
UPLOAD_FOLDER = "uploads"

# Create folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Sidebar
st.sidebar.title("📁 Dashboard")
st.sidebar.write("Mini Google Drive")
st.sidebar.write("Manage your files easily")

file_count = len(os.listdir(UPLOAD_FOLDER))
st.sidebar.metric("Total Files", file_count)

# Title
st.title("☁ Mini Google Drive")

# Multiple file upload
uploaded_files = st.file_uploader(
    "Upload files",
    accept_multiple_files=True
)

# Save uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"{uploaded_file.name} uploaded successfully!")

# Search bar
search = st.text_input("🔎 Search files")

st.subheader("Stored Files")

files = os.listdir(UPLOAD_FOLDER)

# Filter files if searching
if search:
    files = [file for file in files if search.lower() in file.lower()]

# Display files
for file in files:

    col1, col2, col3 = st.columns(3)

    file_path = os.path.join(UPLOAD_FOLDER, file)

    with col1:
        size = os.path.getsize(file_path) / 1024
        st.write(f"{file} ({size:.2f} KB)")

        # Image preview
        if file.endswith(("png", "jpg", "jpeg")):
            st.image(file_path, width=150)

    with col2:
        with open(file_path, "rb") as f:
            st.download_button("Download", f, file_name=file)

    with col3:
        if st.button("Delete", key=file):
            os.remove(file_path)
            st.rerun()