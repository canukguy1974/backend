from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.google_docs import router as google_docs_router
from routes.sop_routes import router as sop_router
from pydantic import BaseModel

app = FastAPI()  # ✅ This must come before using @app decorators
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or "*" while testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(google_docs_router)
app.include_router(sop_router)

# Health check
@app.get("/")
def read_root():
    return {"status": "AI Agent Backend Online"}

# Proposal generation model + route
class ProposalRequest(BaseModel):
    industry: str
    goal: str
    tone: str

@app.post("/api/generate-proposal")
async def generate_proposal(data: ProposalRequest):
    # This is a dummy response – replace with actual AI call later
    response = f"""
    🧠 Proposal for {data.industry}

    Goal: {data.goal}
    Tone: {data.tone}

    Here's a quick overview of our AI-powered proposal for boosting your business.
    """
    return {"proposal": response.strip()}
