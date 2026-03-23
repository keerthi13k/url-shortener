from fastapi import FastAPI
from app.database import engine, Base
from app import routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener",
    description="A production-grade URL shortener with analytics",
    version="1.0.0"
)

app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "URL Shortener is running"}