import uvicorn

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def home():
    return {"Welcome"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
