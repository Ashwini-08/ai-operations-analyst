from fastapi import FastAPI

from app.database import check_database_connection
from app.routes.analytics import router as analytics_router
from app.routes.investigations import router as investigations_router

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


@app.get("/health/db")
def database_health_check():
    is_connected = check_database_connection()

    if is_connected:
        return {
            "status": "ok",
            "database": "connected"
        }

    return {
        "status": "error",
        "database": "not connected"
    }


app.include_router(analytics_router)
app.include_router(investigations_router)