
import tempfile
import streamlit as st
import os

temp_directory = "uploaded_temp_files"

def save_uploaded_file(uploaded_file, directory=temp_directory):
    # Create the directory if it doesn't exist
    try:
        os.makedirs(directory, exist_ok=True)

        # Create the full file path
        file_path = os.path.join(directory, uploaded_file.name)

        # Write the file
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())
        return file_path

    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def delete_uploaded_file(file_path):
    try:
        os.unlink(file_path)
    except Exception as e:
        st.error(f"Error deleting file: {e}")
        return None