from fastapi import APIRouter
from pydantic import BaseModel
from agents.sop_agent import generate_sop, sop_to_text

router = APIRouter()

class SOPRequest(BaseModel):
    business_name: str
    department: str
    author: str

@router.post("/api/generate-sop")
def generate_sop_endpoint(data: SOPRequest):
    sop_doc = generate_sop(
        business_name=data.business_name,
        department=data.department,
        author=data.author
    )
    text = sop_to_text(sop_doc)
    return {"sop": text}
