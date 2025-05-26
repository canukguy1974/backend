from fastapi import FastAPI
from pydantic import BaseModel
from sop_agent import get_sop_agent
from routes.google_docs import router as google_docs_router

app = FastAPI()
app.include_router(google_docs_router)
agent = get_sop_agent()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_sop(question: Question):
    answer = agent.run(question.query)
    return {"answer": answer}
