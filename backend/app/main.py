from fastapi import FastAPI
from .agent.routes import router

app = FastAPI(title="AI Resource Hub")


@app.get("/health")
def health_check():
    return {"status": "ok"}

#TODO ensure that all routes here are gated by authentication
app.include_router(router, prefix="/chat")