import requests
import json
import base64
import os

def get_ticket_info(ticket_id):

    # Base encode email and api token
    key = os.getenv("JIRA_API_KEY")
    user = os.getenv("JIRA_API_USER")
    cred =  "Basic " + base64.b64encode(bytes(user+":"+key, 'utf-8')).decode("utf-8")
    # Set header parameters
    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
       "Authorization" : cred
    }

    # Update your site url
    url = "https://tillerlock.atlassian.net/rest/api/3/issue/" + str(ticket_id)

    # Send request and get response
    response = requests.request(
       "GET",
       url,
       headers=headers
    )
    if int(response.status_code) != 200:
        print(f"Error finding ticket. Return code: {response.status_code}")
        return None

    # Decode Json string to Python
    json_data = json.loads(response.text)

    return  json_data['fields']['summary']
