from fastapi import FastAPI, status, HTTPException, Depends
from .database import engine, get_db
from . import models, schemas, utils
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends((get_db))):
    post = db.query(models.Post).all()
    print(db.query(models.Post))
    return {post}

#Extend pydantic BaseModel

my_posts = ""

def find_post(id):
    for p in my_posts:
        if p['id'] == int(id):
            return p

def find_id_index(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends((get_db))):
    post = db.query(models.Post).all()
    return post

@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends((get_db))):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print('----', post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} was not found.')
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends((get_db))):
    # tedious to mention all the attributes while inserting (E.g. below)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # Best Approach: unpack the pydantic model "post" and insert
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Funtions as Postgres RETURNING stmt
    return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends((get_db))):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")

    deleted_post.delete(synchronize_session=False)
    db.commit()

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends((get_db))):
    query = db.query(models.Post).filter(models.Post.id == id)
    update_post = query.first()
    #find if an entry with the given ID exists
    if update_post is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")

    query.update(post.dict(), synchronize_session=False)
    db.commit()

    return query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends((get_db))):
    # hast the password - user.password
    user.password = utils.hash(user.password)

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Funtions as Postgres RETURNING stmt

    return new_user

@app.get("/users/{id}", response_model=schemas.UserCreateResponse)
def get_users(id: int, db: Session = Depends((get_db))):
    users = db.query(models.Users).filter(models.Users.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return users