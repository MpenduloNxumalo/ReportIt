from fastapi import status, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from models.report_it_models import *
from utils.controller_utils import get_db

router = APIRouter()

@router.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = UserModel(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user

@router.get("/retrieve_users")
def retrieve_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.get("/retrieve_user/{id}")
def retrieve_user(id, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    return user

@router.put("/update_user/{id}")
def update_user(id, request_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id)
    if not user.first():
        return {"isSuccess": False}
    user.update(request_user.model_dump())
    db.commit()
    return {"isSuccess": True}

@router.delete("/delete_user/{id}")
def delete_user(id, db: Session = Depends(get_db)):
    db.query(UserModel).filter(UserModel.id == id).delete(synchronize_session=False)
    db.commit()
    return {"isSuccess": True}