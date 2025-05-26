from fastapi import FastAPI
from pydantic import BaseModel
from agents.sop_agent import generate_sop, sop_to_text
from routes.google_docs import router as google_docs_router
from routes.sop_routes import router as sop_router

app.include_router(sop_router)
app = FastAPI()
app.include_router(google_docs_router)
agent = get_sop_agent()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_sop(question: Question):
    answer = agent.run(question.query)
    return {"answer": answer}
    
    app.get("/")
def read_root():
    return {"status": "AI Agent Backend Online"}
