import json
import subprocess

class SharePoint:
    def __init__(self, client_id, client_secret, site_url, list_name):
        self.client_id = client_id
        self.client_secret = client_secret
        self.site_url = site_url
        self.list_name = list_name

    def get_list_item(self, name):

        # Define the Pnp.PowerShell command to execute
        command = f"""
        $ClientId = "{self.client_id}"
        $ClientSecret = "{self.client_secret}"
        $SiteUrl = "{self.site_url}"
        $ListName = "{self.list_name}"
        $Name = '{name}'

        Try {{
        Import-Module -Name PnP.PowerShell
        # Connect to the SharePoint site
        Connect-PnPOnline -Url $siteUrl -ClientId $clientId -ClientSecret $clientSecret -WarningAction Ignore

        # Retrieve item from SharePoint list
        $Query = "<View><Query><Where><Eq><FieldRef Name='RequestorName'/><Value Type='Text'>$Name</Value></Eq></Where><OrderBy><FieldRef Name='ID' Ascending='FALSE'/></OrderBy></Query><RowLimit>10</RowLimit></View>"
        $ListItems = Get-PnPListItem -List $ListName -Query $Query | Select @{{Label="ID";Expression={{$_.Id}}}}, @{{Label="RequestorName";Expression={{$_.FieldValues.RequestorName}}}}, @{{Label="AppName";Expression={{$_.FieldValues.AppName}}}}, @{{Label="Description";Expression={{$_.FieldValues.Description}}}}, @{{Label="Version";Expression={{$_.FieldValues.Version_x0023_}}}}
        $ListItems = $ListItems | ConvertTo-Json -Compress
        return $ListItems
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
        print('Add List Item Output: ', output)
        return output

    def add_item_to_list(self, data):
        # Convert the item dictionary to a JSON string
        item_json = json.dumps(data)

        # Define the PowerShell command
        command = f"""
        $clientId = "{self.client_id}"
        $clientSecret = "{self.client_secret}"
        $siteUrl = "{self.site_url}"
        $listName = "{self.list_name}"
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
        print('Add List Item Output: ', output)
        return output

    def upload_file_to_list_item(self, item_id, file_path):
        # Define the PowerShell command
        command = f"""
        $ClientId = "{self.client_id}"
        $ClientSecret = "{self.client_secret}"
        $SiteUrl = "{self.site_url}"
        $ListName = "{self.list_name}"
        $ItemId = {item_id}
        $FilePath = ((Get-Location).Path + '\\' + "{file_path}")

        Try {{
            Import-Module -Name PnP.PowerShell
            # Connect to the SharePoint site
            Connect-PnPOnline -Url $SiteUrl -ClientId $ClientId -ClientSecret $ClientSecret -WarningAction Ignore

            # Get the list item
            #$item = Get-PnPListItem -List $listName -Id $itemId

            # Upload the file to the list item
            #Add-PnPListItemAttachment -Id $filePath -Folder ("$listName/Attachments/" + $item.Id)
            Add-PnPListItemAttachment -List $ListName -Identity $ItemID -Path $FilePath
        }}
        Catch {{
            Write-Output $_.Exception.Message
            Write-Output ("File Path: $FilePath")
            Write-Output ("Location: {{0}}" -f (Get-Location).Path)
        }}
        """

        # Run the PowerShell command
        process = subprocess.Popen(["pwsh", "-Command", command], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        output = output.decode().strip()
        print('Upload File Output: ', output)
        return output

    def remove_list_item(self, item_id):
        # Define the PowerShell command
        command = f"""
        $ClientId = "{self.client_id}"
        $ClientSecret = "{self.client_secret}"
        $SiteUrl = "{self.site_url}"
        $ListName = "{self.list_name}"
        $ItemId = {item_id}

        Try {{
        Import-Module -Name PnP.PowerShell
        # Connect to the SharePoint site
        Connect-PnPOnline -Url $siteUrl -ClientId $clientId -ClientSecret $clientSecret -WarningAction Ignore

        # Remove the item from the SharePoint list
        Remove-PnPListItem -List $ListName -Identity $ItemId -Force
        return $true
        }}
        Catch {{
            Write-OutPut $_.Exception.Message
            return $false
        }}
        """

        # Run the PowerShell command
        process = subprocess.Popen(["pwsh", "-Command", command], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        output = output.decode().strip()
        print('Remove List Item Output: ', output)
        return output
