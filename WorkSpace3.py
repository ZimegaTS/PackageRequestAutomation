#import requests
#from requests.auth import HTTPBasicAuth
#client_id = "e73e0af6-259c-4d14-bc88-8375aa693230"
#client_id = "f3ed1a5c-2a9a-430f-aa8f-ede1b2e22593"
#client_secret = "y808Q~SqhOWnxu7EJww4tkQpzK0t-Y-VRS.uGdBU"
#client_secret = "IiO8Q~QHWuf46XOjUhXtEr~YuNGlaXHNBVeW6ccz"
import json
class SharePoint:
    def __init__(self, client_id, client_secret, tenant_id, site_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.site_url = site_url

    def add_item_to_list(self, list_name, data):
        access_token = self.get_access_token()
        if access_token is None:
            print("Failed to get access token")
            return None
        else:
            print("Access token:", access_token)
        headers = {
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json;odata=verbose",
            "Content-Type": "application/json"
        }
        try:
            json.dumps(data)
            print("Data is serializable")
        except (TypeError, OverflowError) as e:
            print("Error: data cannot be serialized into a JSON object:", e)
            return None
        print("Data:", json.dumps(data))
        api_url = f"{self.site_url}/_api/web/lists/getbytitle('{list_name}')/items"
        print("API URL:", api_url)
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            #print("Item added successfully.")
            #return response.json()['d']['Id']
            print("Item added successfully. Response:", response.json())
            return response.json().get('d', {}).get('Id')
        else:
            print("Status Code: ", response.status_code, "\nError: ", response)
            return None

    def upload_file_to_list_item(self, list_name, item_id, file_path):
        access_token = self.get_access_token()
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Accept': 'application/json;odata=verbose'
        }
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as file_data:
            response = requests.post(f"{self.site_url}/_api/web/lists/getbytitle('{list_name}')/items({item_id})/AttachmentFiles/add(FileName='{file_name}')",
                                     headers=headers, data=file_data)
        if response.status_code == 200:
            print("File uploaded successfully")
        else:
            print("Error: ", response.text)
