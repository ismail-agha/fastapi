from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends((get_db))):
    # hast the password - user.password
    user.password = utils.hash(user.password)

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Funtions as Postgres RETURNING stmt

    return new_user

@router.get("/{id}", response_model=schemas.UserCreateResponse)
def get_users(id: int, db: Session = Depends((get_db))):
    users = db.query(models.Users).filter(models.Users.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return users