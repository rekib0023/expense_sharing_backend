import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app import models
from app.routers import authentication, user
from db import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router, tags=["Auth"], prefix="/api/auth")
app.include_router(user.router, tags=["User"], prefix="/api/user")


@app.get("/api/healthchecker")
def root():
    return {"message": "Hello World"}


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
