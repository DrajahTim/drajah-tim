from fastapi import FastAPI
from backend.core.config import settings
from backend.routers import auth # Import the auth router
# from backend.core.database import create_db_and_tables # For initial table creation if not using Alembic

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json" # Standardize OpenAPI doc URL
)

# Include routers
app.include_router(auth.router)
# app.include_router(users_router, prefix=settings.API_V1_STR, tags=["Users"]) # Example for other routers
# app.include_router(queues_router, prefix=settings.API_V1_STR, tags=["Queues"])


@app.on_event("startup")
async def startup_event():
    # This is an example if you wanted to create tables on startup without Alembic
    # Be cautious with this in production. Alembic is preferred.
    # print("Creating database tables...")
    # await create_db_and_tables() # Make sure your models are imported in models/__init__
    # print("Database tables created (if they didn't exist).")
    pass

@app.get(f"{settings.API_V1_STR}/healthcheck")
async def health_check():
    return {"status": "ok", "message": f"Welcome to {settings.PROJECT_NAME}"}


if __name__ == "__main__":
    import uvicorn
    # For development, run with uvicorn main:app --reload from the backend directory
    uvicorn.run(app, host="0.0.0.0", port=8000)
