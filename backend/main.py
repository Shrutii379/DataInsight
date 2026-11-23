
from fastapi import FastAPI
from backend.routes.analytics import router as analytics_router

app = FastAPI(
    title="DataInsight API",
    description="E-Commerce Analytics Backend",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to DataInsight API!",
        "status": "Backend is running successfully"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Register analytics routes
app.include_router(
    analytics_router,
    prefix="/api",
    tags=["Analytics"]
)
