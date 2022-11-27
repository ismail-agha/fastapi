from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from typing import List, Optional

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends((get_db)), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print("limit=", limit)
    #post = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search))\
        .limit(limit).offset(skip).all()
    return post

@router.get("/postvote", response_model=List[schemas.PostVote])
def get_postvotes(db: Session = Depends((get_db)), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    query = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).\
        join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    print(query)
    results = query.all()
    return results

@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends((get_db)), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} was not found.')
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends((get_db)),
                current_user: int = Depends(oauth2.get_current_user)):
    # tedious to mention all the attributes while inserting (E.g. below)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # Best Approach: unpack the pydantic model "post" and insert

    print(current_user)
    print(current_user.email)
    print(post)

    #new_post = models.Post(**post.dict())

    #post_dict = post.dict()
    #post_dict['owner_id'] = current_user.id
    #new_post = models.Post(**post_dict) #models.Post(**post.dict())

    new_post = models.Post(owner_id=current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Funtions as Postgres RETURNING stmt
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends((get_db)),
                current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")

    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorise to perform requested action")

    deleted_post.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends((get_db)),
                current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    update_post = query.first()
    #find if an entry with the given ID exists
    if update_post is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id:{id} does not exist")

    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorise to perform requested action")

    query.update(post.dict(), synchronize_session=False)
    db.commit()

    return query.first()