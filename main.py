import requests
from requests.auth import HTTPBasicAuth
import json

def add_item_to_sharepoint_list(client_id, client_secret, tenant_id, site_url, list_name):
    # Get access token
    token_url = f"https://accounts.accesscontrol.windows.net/{tenant_id}/tokens/OAuth/2"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': '00000003-0000-0ff1-ce00-000000000000/sharepoint.com@' + tenant_id
    }
    token_response = requests.post(token_url, data=payload)
    access_token = token_response.json().get("access_token")

    # Define headers
    headers = {
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose"
    }

    # Define API endpoint
    api_url = f"{site_url}/_api/web/lists/getbytitle('{list_name}')/items"

    # Data to add
    data = {
        '__metadata': {'type': 'SP.Data.YourListNameListItem'},  # Replace YourListName with your list name
        'Title': 'Cisco Client',
        'Description': 'Here is the Description',
        'Keywords': 'Keyword1, Keyword2',
        'Version_x0023_': '1.00.0000'  # SharePoint internal field names may vary
    }

    # Make the POST request
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print("Item added successfully.")
    else:
        print("Error: ", response.text)

# Example usage
client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"
site_url = "https://yourcompany.sharepoint.com/sites/yoursite"
list_name = "YourListName"

add_item_to_sharepoint_list(client_id, client_secret, tenant_id, site_url, list_name)
