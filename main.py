from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

from router.airtable_router import router as airtable_router
from router.notion_router import router as notion_router
from router.hubspot_router import router as hubspot_router

# CORS configuration
origins = [
    "http://localhost:3000",  # React app address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

#Routes
app.include_router(airtable_router)
app.include_router(notion_router)
app.include_router(hubspot_router)
