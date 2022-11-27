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

my_posts = ""

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
    cursor.execute(""" SELECT * FROM posts """)
    post = cursor.fetchall()
    return {'data': post}

@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id), ))
    post = cursor.fetchall()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} was not found.')
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    #Parametrized Query
    cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"New_Post": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *""",
                   (post.title, post.content, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")

    return {"Updated Post": updated_post}


