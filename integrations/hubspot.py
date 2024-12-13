# hubspot.py

import os
import json
import secrets
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import base64
import requests
from integrations.integration_item import IntegrationItem
from redis_client import add_key_value_redis, get_value_redis, delete_key_redis

CLIENT_ID = os.getenv('CLIENT_ID')
HUBSPOT_APP_ID = os.getenv('HUBSPOT_APP_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
AUTHORIZATION_URI = os.getenv('AUTHORIZATION_URI')
REDIRECT_URI= os.getenv('REDIRECT_URI')
SCOPE = os.getenv('SCOPE')

async def authorize_hubspot(user_id, org_id):
    state_data = {
        'state': secrets.token_urlsafe(32), #Randomly generated string
        'user_id': user_id,
        'org_id': org_id,
    }

    #Encodes state_data as a Base64 string for safe inclusion in the URL.
    encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode('utf-8')).decode('utf-8')

    #Construct the HubSpot authorization URL with necessary query parameters.
    auth_url = f'{AUTHORIZATION_URI}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}&state={encoded_state}'

    #Stores the state_data in Redis with a 10-minute expiration.
    await asyncio.gather(
        add_key_value_redis(f'hubspot_state:{org_id}:{user_id}', json.dumps(state_data), expire=600),
    )
    return auth_url

# Redirection funtion from hubsport after authorization 
async def oauth2callback_hubspot(request: Request):
    if request.query_params.get('error'):
        raise HTTPException(status_code=400, detail=request.query_params.get('error_description'))

    # Extracts the code and state from the query parameters and decodes the state.
    code = request.query_params.get('code')
    encoded_state = request.query_params.get('state')
    state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode('utf-8'))
    original_state = state_data.get('state')
    user_id = state_data.get('user_id')
    org_id = state_data.get('org_id')

    saved_state = await asyncio.gather(
        get_value_redis(f'hubspot_state:{org_id}:{user_id}')
    )

    #Validate the state to ensure it matches the original value.
    if not saved_state or original_state != json.loads(saved_state[0]).get('state'):
        raise HTTPException(status_code=400, detail='State does not match.')

    #Send a request to HubSpot to exchange the authorization code for an access token and deletes the Redis state
    async with httpx.AsyncClient() as client:
        response, _ = await asyncio.gather(
            client.post(
                'https://api.hubapi.com/oauth/v1/token',
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': REDIRECT_URI,
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET
                },
            ),
            delete_key_redis(f'hubspot_state:{org_id}:{user_id}'),
        )

    # Storing the credentials
    await add_key_value_redis(f'hubspot_credentials:{org_id}:{user_id}', json.dumps(response.json()), expire=600)

    #Send the HTMLResponse to close the hubspot authorization popup
    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)

# Fetches and deletes the user's HubSpot credentials from Redis.
async def get_hubspot_credentials(user_id, org_id):
    credentials = await get_value_redis(f'hubspot_credentials:{org_id}:{user_id}')

    if not credentials:
        raise HTTPException(status_code=400, detail='No credentials found.')

    credentials = json.loads(credentials)

    await delete_key_redis(f'hubspot_credentials:{org_id}:{user_id}')

    return credentials

# Creates an IntegrationItem object using data from HubSpot's response.
def create_integration_item_metadata_object(response_json) -> IntegrationItem:
    users_integration_item_metadata = IntegrationItem(
        id=response_json.get('id'),
        creation_time=response_json.get('properties').get('createdate'),
        last_modified_time=response_json.get('properties').get('updatedAt'),
        firstName=response_json.get('properties').get('firstname'),
        lastName=response_json.get('properties').get('lastname'),
        email=response_json.get('properties').get('email'),
        archived=response_json.get('archived'),
    )
    return users_integration_item_metadata

async def get_items_hubspot(credentials):
    # Define the API endpoint and authorization headers.
    credentials = json.loads(credentials)
    url = 'https://api.hubapi.com/crm/v3/objects/users'
    headers = {'Authorization': f'Bearer {credentials.get("access_token")}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        #Retrieve the 'results'
        result = response.json().get('results', [])
        users_integration_item_metadata = [
            create_integration_item_metadata_object(item) for item in result
        ]
        print(f'users_integration_item_metadata: {users_integration_item_metadata}')
        return users_integration_item_metadata
    else:
        return []