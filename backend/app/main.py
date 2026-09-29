from fastapi import FastAPI

app = FastAPI(title="AI Resource Hub")


@app.get("/health")
def health_check():
    return {"status": "ok"}
