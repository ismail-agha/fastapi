from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

#Extend pydantic BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {id: 1 , "title": "title of post 1", "content": "content of post 1"},
    {id: 2 , "title": "favorite foods", "content": "I like pizza"}
]

@app.post("/posts")
def create_post(new_payload: Post):
    print(new_payload)
    print(new_payload.dict())
    return {"message":f"Title: {new_payload.title} | Content: {new_payload.content}"}