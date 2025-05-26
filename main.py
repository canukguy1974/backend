from fastapi import FastAPI
from routes.google_docs import router as google_docs_router
from routes.sop_routes import router as sop_router

app = FastAPI()

# Include routers
app.include_router(google_docs_router)
app.include_router(sop_router)

# Health check
@app.get("/")
def read_root():
    return {"status": "AI Agent Backend Online"}
