from fastapi import FastAPI

app = FastAPI(
    title="AI Operations Analyst API",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "message": "AI Operations Analyst API is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Operations Analyst API",
        "version": "0.1.0"
    }