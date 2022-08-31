import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from db import db
from app.routes import authentication


app = FastAPI()


app.include_router(authentication.router, prefix="/api")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
