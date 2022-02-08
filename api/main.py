from fastapi import FastAPI
from routers import encryption


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Microservices!"}


app.include_router(encryption.router)
