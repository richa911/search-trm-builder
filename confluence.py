import time
import requests
import json
from util import monday_730
from datetime import datetime
from requests.auth import HTTPBasicAuth
import config
from decouple import config as configEnv

# URL for the Confluence API
CONFLUENT_API_URL = 'https://swiggy.atlassian.net/wiki/api/v2/pages'
# Base URL for the Confluence API
base_url = 'https://swiggy.atlassian.net'
# Date format to be used in the page title
DATE_FORMAT = '%d %b %Y'
# Error message template
ERROR_MSG = "Error: {}"
# Success message for page creation
PAGE_CREATED_MSG = 'Page Created!'
# Error message for unexpected response
UNEXPECTED_RESPONSE_MSG = "Error: Unexpected response {}"


from datetime import datetime

def format_date_with_suffix(date):
    """
    Format a datetime object to 'Month DaySuffix' (e.g., 'Mar 24th').
    """
    day = date.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return date.strftime(f"%b {day}{suffix}")

def generate_title(start_ms, end_ms):
    """
    Generate a title for the Confluence page.

    Parameters:
    start_ms (int): The start date in milliseconds since the epoch
    end_ms (int): The end date in milliseconds since the epoch

    Returns:
    str: The generated title
    """
    start_date = format_date_with_suffix(datetime.utcfromtimestamp(start_ms / 1000))
    end_date = format_date_with_suffix(datetime.utcfromtimestamp((end_ms / 1000) - 86400))
    
    return f"Search | {start_date} - {end_date}"


def create_confluence_page(parent_page_id, email_id, auth_token, html_content, space_id):
    """
    Create a new Confluence page.

    Parameters:
    parent_page_id (str): The ID of the parent page
    email_id (str): The email ID for authentication
    auth_token (str): The authentication token
    html_content (str): The HTML content of the page
    space_id (str): The ID of the space where the page will be created

    Returns:
    None
    """
    start, end = monday_730(current_week=False), monday_730(current_week=True)
    page_title = generate_title(start, end)

    auth = HTTPBasicAuth(email_id, auth_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "user-agent": "API"
    }

    payload = json.dumps({
        "spaceId": space_id,
        "status": "draft",
        "title": page_title,
        "parentId": parent_page_id,
        "body": {
            "representation": "storage",
            "value": html_content
        }
    })
    try:
        r = requests.request(
            "POST",
            CONFLUENT_API_URL,
            data=payload,
            headers=headers,
            auth=auth
        )

        if not r.status_code // 100 == 2:
            print(UNEXPECTED_RESPONSE_MSG.format(r.content))
        else:
            links = r.json()['_links']
            page_id = r.json()['id']
            print(PAGE_CREATED_MSG + "ID: " + page_id + " - " + links['base'] + links['editui'])
            return page_id

    except requests.exceptions.RequestException as e:
        print(ERROR_MSG.format(e))


def update_confluence_page(page_id, email_id, auth_token, html_content):
    """
    Update an existing Confluence page.

    Parameters:
    page_id (str): The ID of the page to be updated
    email_id (str): The email ID for authentication
    auth_token (str): The authentication token
    html_content (str): The HTML content to be updated

    Returns:
    None
    """
    start, end = monday_730(current_week=False), monday_730(current_week=True)
    page_title = generate_title(start, end)
    url = f"{base_url}/wiki/api/v2/pages/{page_id}"
    auth = HTTPBasicAuth(email_id, auth_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "user-agent": "API"
    }

    payload = json.dumps({
        "id": str(page_id),
        "status": "draft",
        "title": page_title,
        "body": {
            "representation": "storage",
            "value": html_content
        },
        "version": {
            "number": 1,
            "message": "Updated Page"
        }
    })
    try:
        r = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        if not r.status_code // 100 == 2:
            print(UNEXPECTED_RESPONSE_MSG.format(r.content))
        else:
            print("Page Updated!")

    except requests.exceptions.RequestException as e:
        print(ERROR_MSG.format(e))


def upload_image_attachment(filename, page_id, comment=""):
    """
    Upload an attachment to a Confluence page.

    Parameters:
    filename (str): The name of the file to be uploaded
    page_id (str): The ID of the page
    comment (str): The comment for the

    Returns:
    link of the attachment
    """
    url = "https://swiggy.atlassian.net/wiki/rest/api/content/" + str(page_id) + "/child/attachment"

    payload = {'minorEdits': 'true', 'comment': comment}
    files = [
        ('file', (str(time.time()) + '.png', open(
            filename,
            'rb'), 'image/png'))
    ]
    headers = {
        'X-Atlassian-Token': 'nocheck'
    }
    auth = HTTPBasicAuth(config.emailID, configEnv('CONFLUENT_PAGE_AUTH_TOKEN'))

    response = requests.request("POST", url, headers=headers, data=payload, files=files, auth=auth,
                                params={'status': 'draft'})

    if not response.status_code // 100 == 2:
        print(UNEXPECTED_RESPONSE_MSG.format(response.content))
    else:
        attachment_filename = response.json()['results'][0]['title']
        # print("Attachment Uploaded: " + attachment_filename)
        return attachment_filename
