from fastapi import FastAPI

app = FastAPI(title="QueueMe API", version="0.1.0")

@app.get("/")
async def read_root():
    return {"message": "Welcome to QueueMe API"}

# Further routers will be included here
# e.g., from routers import queues, users
# app.include_router(queues.router)
# app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
