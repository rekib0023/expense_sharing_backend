import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session as db, close_all_sessions
from app.routes import authentication
from app import models
from db import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(authentication.router, prefix="/api")




@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
