from fastapi import APIRouter, Form, Request
from integrations.hubspot import authorize_hubspot, get_hubspot_credentials, get_items_hubspot, oauth2callback_hubspot

router = APIRouter()

@router.post('/integrations/hubspot/authorize')
async def authorize_hubspot_integration(user_id: str = Form(...), org_id: str = Form(...)):
    return await authorize_hubspot(user_id, org_id)

@router.get('/integrations/hubspot/oauth2callback')
async def oauth2callback_hubspot_integration(request: Request):
    return await oauth2callback_hubspot(request)

@router.post('/integrations/hubspot/credentials')
async def get_hubspot_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
    return await get_hubspot_credentials(user_id, org_id)

@router.post('/integrations/hubspot/get_hubspot_items')
async def load_hubspot_items(credentials: str = Form(...)):
    return await get_items_hubspot(credentials)
