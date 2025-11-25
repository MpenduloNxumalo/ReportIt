from fastapi import APIRouter
from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from models.report_it_models import *
from utils.controller_utils import get_db

router = APIRouter()

@router.post("/create_location",status_code=status.HTTP_201_CREATED)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    new_location = LocationModel(
        latitude=location.latitude,
        longitude=location.longitude,
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location

@router.get("/retrieve_locations")
def retrieve_all_locations(db: Session = Depends(get_db)):
    locations = db.query(LocationModel).all()
    return locations

@router.get("/retrieve_location/{id}")
def retrieve_location(id, db: Session = Depends(get_db)):
    location = db.query(LocationModel).filter(LocationModel.id == id).first()
    return location

@router.put("/update_location/{id}")
def update_location(id, request_user: schemas.UserCreate, db: Session = Depends(get_db)):
    location = db.query(LocationModel).filter(LocationModel.id == id)
    if not location.first():
        return {"isSuccess": False}
    location.update(request_user.model_dump())
    db.commit()
    return {"isSuccess": True}

@router.delete("/delete_location/{id}")
def delete_location(id, db: Session = Depends(get_db)):
    db.query(LocationModel).filter(LocationModel.id == id).delete(synchronize_session=False)
    db.commit()
    return {"isSuccess": True}