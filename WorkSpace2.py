import subprocess
import json

client_id = "224bebab-1cd8-4ecd-ad0a-22a24eec0637"
client_secret = "Ypv+1gYbznor07Yjg9Cc0v9BmF8zwKic0/fJhPTry/U="
tenant_id = "2865f772-ad7a-44d0-bbfb-c6dcf729471a"
site_url = "https://zimegats.sharepoint.com/sites/PackageAutomation"
list_name = "PackageAutomationList"




def add_sharepoint_list_item(client_id, client_secret, site_url, list_name, item):
    # Convert the item dictionary to a JSON string
    item_json = json.dumps(item)

    # Define the PowerShell command
    command = f"""
    $clientId = "{client_id}"
    $clientSecret = "{client_secret}"
    $siteUrl = "{site_url}"
    $listName = "{list_name}"
    $item = '{item_json}'

    Try {{
    Import-Module -Name PnP.PowerShell
    # Connect to the SharePoint site
    Connect-PnPOnline -Url $siteUrl -ClientId $clientId -ClientSecret $clientSecret -WarningAction Ignore

    # Convert the item JSON string to a PowerShell hashtable
    $itemHashtable = ConvertFrom-Json $item -AsHashtable

    # Add the item to the SharePoint list
    $addedItem = Add-PnPListItem -List $listName -Values $itemHashtable
    return $addedItem.Id
    }}
    Catch {{
        Write-OutPut $_.Exception.Message
        return $null
    }}
    """

    # Run the PowerShell command
    process = subprocess.Popen(["pwsh", "-Command", command], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    output = output.decode().strip()
    print('Output: ', output)
    return output

# Example usage
item = {
        'Title': 'Brave',
        'Description': 'Here is the Description',
        'Keywords': 'Keyword1, Keyword2',
        'Version_x0023_': '1.00.0000'
}
item_id = add_sharepoint_list_item(client_id, client_secret, site_url, list_name, item)

print("Item ID:", item_id)
