"""
The configuration file would look like this (sans those // comments):

{
    "authority": "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here",
    "client_id": "your_client_id",
    "scope": ["https://graph.microsoft.com/.default"],
        // For more information about scopes for an app, refer:
        // https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow#second-case-access-token-request-with-a-certificate"

    "secret": "The secret generated by AAD during your confidential app registration",
        // For information about generating client secret, refer:
        // https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki/Client-Credentials#registering-client-secrets-using-the-application-registration-portal

    "endpoint": "https://graph.microsoft.com/v1.0/users"

}



You can then run this sample with a JSON configuration file:

    python sample.py parameters.json

In parameters.json FOR ACCESSING  FILE FROM ONRDRIVE use
    "endpoint": "https://graph.microsoft.com/v1.0/users/c67255c9-a875-4951-9d2a-0c6ed8a5a8d1/drive/root:/Book1.xlsx:/workbook/worksheets('Sheet2')/usedRange

    user id = You can get user id by running "https://graph.microsoft.com/v1.0/me/"  OR "https://graph.microsoft.com/v1.0/me/drive/root/children"
    query on graph explorer
    **Signin to graph explorer using the same account whoes client id and secret you are using


"""
# Rohan sir creds
# {  
#   "authority": "https://login.microsoftonline.com/ad0484b5-feb5-4f95-949f-a9cbe7a34294",
#   "client_id": "f6b48f58-a5a0-4ba6-b0cd-efecddaddb25",
#   "scope": [ "https://graph.microsoft.com/.default" ],
#   "secret": "xZHO0Rfsue~SD.BuZ7OiAyi18LL3F._NYI",
#   "endpoint": "https://graph.microsoft.com/v1.0/users/"
# }

# Shruti Purandare creds
# {
#   "authority": "https://login.microsoftonline.com/cb708b7c-cfaf-4aef-8e57-a5a046700dfc",
#   "client_id": "9b963eb9-734a-44f9-af8f-f8556c2f23a1",
#   "scope": [ "https://graph.microsoft.com/.default" ],
#   "secret": "KbN2JiePL_~tP0vTO9.aq.wREx1Ynf0A0C",
#   "endpoint": "https://graph.microsoft.com/v1.0/users/"

#   "endpoint": "https://graph.microsoft.com/v1.0/me/drive/root:/book1.xlsx:/workbook/worksheets('Sheet2')/range(address='A1:C7')"
# }


import sys  # For simplicity, we can read config file from 1st CLI param sys.argv[1]
import json
import logging

import requests
import msal

#  https://graph.microsoft.com/v1.0/users/shrutipurandare812@gmail.onmicrosoft.com/drive/root/children


# Optional logging
# logging.basicConfig(level=logging.DEBUG)


# opening parameters.json and storing it in config variable
config = json.load(open('1-Call-MsGraph-WithSecret\parameters.json'))

"""
If you use 
 config = json.load(open(sys.argv[1]))
 You should pass name of file which contains all parameters as command line argument
"""

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"],
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

# The pattern to acquire a token looks like this.
result = None
accessToken=None
data=None

print("Id: "+config["client_id"]+"\n Secret: "+config["secret"]+"\nAuth::"+config["authority"])

# Firstly, looks up a token from cache
# Since we are looking for token for the current app, NOT for an end user,
# notice we give account parameter as None.
result = app.acquire_token_silent(config["scope"], account=None)
print(result)
# result is none

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])
    print(result)
    # accesstoken is acquired
    accessToken=result['access_token']
        
if "access_token" in result:
    # Calling graph using the access token
    graph_data = requests.get(  # Use token to call downstream service
        config["endpoint"],
        headers={'Authorization': 'Bearer ' + result['access_token']}, ).json() 
        #api call converting result to json and storing it to graph data
        
    # if(graph_data!=NULL)        
    print("Graph API call result: ")
    print("@@@@@@@@@@@@",json.dumps(graph_data, indent=2))
    # print(graph_data["values"])
  
  
  
    # Storing result of API call(graph_data(values)) into a file not whole data
    # A Data.json file  will be  created every time you run the program and will store all the file contents  
    

    with open('Data.json', 'w') as f:
        f.write(json.dumps(graph_data["text"], indent=2))
    
    
    #Below code will load whole file into Data.json
    # with open('DataWhole.json', 'w') as f:
    #   f.write(json.dumps(graph_data, indent=2))
    
    
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug
  


"""        
##################################
    Trying To Filter Out Unwanted Data From File
    
    for i in xrange(len(graph_data)):
        if graph_data[i][] == "formulas":
            graph_data.pop(i)
            break
    
    Output the updated file with pretty JSON                                      
    open("updated-file.json", "w").write(
        json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    ) 
    
    ##One more Try
    # Transform json input to python objects
        input_dict = json.loads(graph_data)

    # Filter python objects with list comprehensions
        output_dict = [x for x in input_dict if x['type'] == '1']

    # Transform python object back into json
        output_json = json.dumps(output_dict)

    # Show json
        print(output_json)
######################################
"""       
    
    
# 
# If you're a standard user of your tenant, ask a global administrator to grant admin consent for your application.
# To do this, give the following URL to your administrator:

# https://login.microsoftonline.com/ad0484b5-feb5-4f95-949f-a9cbe7a34294/adminconsent?client_id=cf7f59f2-e388-42fa-961e-fcea02ad66f8