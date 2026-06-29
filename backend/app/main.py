from fastapi import FastAPI

app = FastAPI(
    title="CareLens AI API",
    description="AI-powered Clinical Decision Support & Medical Report Analysis",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to CareLens AI 🚀",
        "status": "Backend is running successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }