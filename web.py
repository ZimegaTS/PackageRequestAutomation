import streamlit as st
from sharepoint import SharePoint
import json
import os
from helpers import save_uploaded_file
from dotenv import load_dotenv
import webbrowser

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
site_url = "https://zimegats.sharepoint.com/sites/PackageAutomation"
list_name = "PackageAutomationList"



sharepoint_item = SharePoint(client_id, client_secret, site_url, list_name)

def main():
    st.title("Package Request Form")
    # create a sidebar
    st.sidebar.title("Previous Requests")

    # Form to gather data
    with st.form(key='sharepoint_form'):
        requestor_name = st.text_input(label='Requestor Name', value='Frank Straughter')
        supervisor_name = st.text_input(label='Supervior Name', value='Frank Straughter')
        application_type = st.selectbox(label='Application Type', options=['Vendor', 'In-House'])
        app_name = st.text_input(label='App Name', value='Cisco Client')
        description = st.text_area(label='Description', value='Here is the Description')
        keywords = st.text_input(label='Keywords', value='Keyword1, Keyword2')
        version = st.text_input(label='Version#', value='1.00.0000')
        uploaded_file = st.file_uploader("Choose a file")

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            with st.spinner("Processing request..." ):
                # Create list item
                data = {
                    'RequestorName': requestor_name,
                    'SupervisorName': supervisor_name,
                    'ApplicationType': application_type,
                    'AppName': app_name,
                    'Description': description,
                    'Keywords': keywords,
                    'Version_x0023_': version
                }
                item_id = sharepoint_item.add_item_to_list(data)
                if item_id is not None:
                    try:
                        if uploaded_file is not None:
                            print("Uploaded File: ", uploaded_file)
                            file_path = save_uploaded_file(uploaded_file)
                            print("File Path: ", file_path)
                            if file_path is not None:
                                #sharepoint_item.upload_file_to_list_item(item_id, file_path)
                                #os.unlink(file_path)  # delete the temporary file
                                st.write("File Uploaded Successfully!")
                    except Exception as e:
                        st.error("Error uploading file: ", e)
                        sharepoint_item.remove_list_item(item_id)
                        st.error("Request Failed!")
                        return
                    st.success("Request Submitted Successfully!")

    with st.sidebar:
        with st.spinner("Loading..."):
            # Get last 10 items from SharePoint list
            items = sharepoint_item.get_list_item('Frank Straughter')
            dict_object = json.loads(items)
        # Display the last 10 items in the sidebar
    
        for item in dict_object:
            app_name = item['AppName']
            version = item['Version']
            description = item['Description']
            item_id = item['ID']
            
            # Create a button with a link to a specific URL
            url = f"{site_url}/lists/{list_name}/DispForm.aspx?ID={item_id}"  # Replace with your desired URL
            if st.sidebar.button(label=f"{app_name} - {version}", key=f"{app_name}-{version}-{item_id}", help="Click to view item on SharePoint"):
                webbrowser.open_new_tab(url)
            # Display the tile
            with st.sidebar:
                st.write('ID: ', str(item_id))
                st.write('Description: ', description)
                st.markdown("---")  # Visual separator


if __name__ == "__main__":
    main()

