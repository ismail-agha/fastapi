from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

#Extend pydantic BaseModel
class Post(BaseModel):
    title: str
    content: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/post/")
async def root():
    return {"message": "Post API"}

@app.post("/createpost")
def create_post(new_payload: Post):
    print(new_payload)
    return {"message":f"Title: {new_payload.title} | Content: {new_payload.content}"}