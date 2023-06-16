import requests
import json
import base64
import os
import logging

def get_ticket_info(ticket_title):

    # Base encode email and api token
    print(f"Gathering ticket info on Jira")
    key = os.getenv("JIRA_API_KEY")
    user = os.getenv("JIRA_API_USER")
    cred =  "Basic " + base64.b64encode(bytes(user+":"+key, 'utf-8')).decode("utf-8")
    # Set header parameters
    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
       "Authorization" : cred
    }

    # get ticket id from title
    colon_index = ticket_title.find(':')
    ticket_id = ticket_title[:colon_index]

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

    print(f"Found ticket {ticket_id} on Jira")
    # Decode Json string to Python
    json_data = json.loads(response.text)
    summary = json_data['fields']['summary']
    description = json_data['fields']['description']['content'][0]['content'][0]['text']
    output_data = [summary, description]

    return  output_data
