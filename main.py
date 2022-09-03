import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app import models
from app.routers import authentication
from db import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(authentication.router, tags=["Auth"], prefix="/api/auth")


@app.get("/api/healthchecker")
def root():
    return {"message": "Hello World"}


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
