from fastapi import FastAPI

app = FastAPI(
    title="AI Support Agent",
    description="AI customer support agent with RAG and human approval",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}