from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Helo Worlddd"}


@app.get("/postss")
def get_posts():
    return {"data": "this is your post"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    return {"new post": f"title {payload['title']}"}
