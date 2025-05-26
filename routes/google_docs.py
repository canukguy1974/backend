from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from utils.gdocs import create_google_doc
from dotenv import load_dotenv
import os, requests

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/oauth2callback")

token_url = "https://oauth2.googleapis.com/token"

tokens = {}  # Replace with a real DB store in production

class ExportRequest(BaseModel):
    sop_text: str

@router.get("/api/oauth2callback")
def oauth2callback(code: str):
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    r = requests.post(token_url, data=data)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="OAuth token exchange failed")
    token_data = r.json()
    tokens["access_token"] = token_data["access_token"]
    return {"message": "OAuth Success. You may now export."}

@router.post("/api/export-doc")
def export_doc(payload: ExportRequest):
    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing OAuth access token")
    doc_id = create_google_doc(access_token, payload.sop_text)
    return {
        "status": "Document created",
        "doc_id": doc_id,
        "url": f"https://docs.google.com/document/d/{doc_id}"
    }
