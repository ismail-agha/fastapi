import time

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
app = FastAPI()

#SET-UP DB Connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='1806@ism', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!!")
        break
    except Exception as error:
        print(f"Database connection Failed. Err : {error}")
        time.sleep(2)

#Extend pydantic BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"id": 1 , "title": "title of post 1", "content": "content of post 1"},
            {"id": 2 , "title": "favorite foods", "content": "I like pizza"}]

def find_post(id):
    for p in my_posts:
        if p['id'] == int(id):
            return p

def find_id_index(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts")
def get_posts():
    return {'data': my_posts}

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} was not found.')
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1, 1000000000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_id_index(id)
    if index is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")
    my_posts.pop(index)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_id_index(id)
    if index is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")

    post = post.dict()
    post["id"] = id
    my_posts[index] = post
    return {"Updated Post": post}

@app.patch("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_id_index(id)
    if index is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")

    post = post.dict()
    post["id"] = id
    my_posts[index] = post
    return {"Updated Post": post}
