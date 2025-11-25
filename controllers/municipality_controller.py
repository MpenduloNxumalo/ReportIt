from fastapi import APIRouter
from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from models.report_it_models import *
from utils.controller_utils import get_db

router = APIRouter()

@router.post("/create_municipality",status_code=status.HTTP_201_CREATED)
def create_municipality(municipality: schemas.MunicipalityCreate, db: Session = Depends(get_db)):
    new_municipality = MunicipalityModel(
        name=municipality.name,
        phone_number=municipality.phone_number,
        location_id=municipality.location_id,
    )
    db.add(new_municipality)
    db.commit()
    db.refresh(new_municipality)
    return new_municipality

@router.get("/retrieve_municipalities")
def retrieve_all_municipalities(db: Session = Depends(get_db)):
    municipalities = db.query(MunicipalityModel).all()
    return municipalities

@router.get("/retrieve_municipality/{id}")
def retrieve_municipality(id, db: Session = Depends(get_db)):
    municipality = db.query(MunicipalityModel).filter(MunicipalityModel.id == id).first()
    return municipality

@router.put("/update_municipality/{id}")
def update_user(id, request_user: schemas.UserCreate, db: Session = Depends(get_db)):
    municipality = db.query(MunicipalityModel).filter(MunicipalityModel.id == id)
    if not municipality.first():
        return {"isSuccess": False}
    municipality.update(request_user.model_dump())
    db.commit()
    return {"isSuccess": True}

@router.delete("/delete_municipality/{id}")
def delete_municipality(id, db: Session = Depends(get_db)):
    db.query(MunicipalityModel).filter(MunicipalityModel.id == id).delete(synchronize_session=False)
    db.commit()
    return {"isSuccess": True}