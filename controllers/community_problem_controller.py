from fastapi import status, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from models.report_it_models import *
from utils.controller_utils import get_db

router = APIRouter()

@router.post("/create_community_problem",status_code=status.HTTP_201_CREATED)
def create_community_problem(community_problem: schemas.CommunityProblemCreate, db: Session = Depends(get_db)):
    new_community_problem = CommunityProblemModel(
        user_id=community_problem.user_id,
        municipal_id=community_problem.municipal_id,
        location_id=community_problem.location_id,
        description=community_problem.description,
        image=community_problem.image,
        date=community_problem.date,
        status=community_problem.status,
    )
    db.add(new_community_problem)
    db.commit()
    db.refresh(new_community_problem)
    return new_community_problem

@router.get("/retrieve_all_community_problems")
def retrieve_all_community_problems(db: Session = Depends(get_db)):
    community_problems = db.query(CommunityProblemModel).all()
    return community_problems

@router.get("/retrieve_community_problem/{id}")
def retrieve_community_problem(id, db: Session = Depends(get_db)):
    community_problem = db.query(CommunityProblemModel).filter(CommunityProblemModel.id == id).first()
    return community_problem

@router.put("/update_community_problem/{id}")
def update_community_problem(id, updated_community_problem: schemas.CommunityProblemCreate, db: Session = Depends(get_db)):
    community_problem = db.query(CommunityProblemModel).filter(CommunityProblemModel.id == id)
    if not community_problem.first():
        return {"isSuccess": False}
    community_problem.update(updated_community_problem.model_dump())
    db.commit()
    return {"isSuccess": True}

@router.delete("/delete_community_problem/{id}")
def delete_community_problem(id, db: Session = Depends(get_db)):
    db.query(CommunityProblemModel).filter(CommunityProblemModel.id == id).delete(synchronize_session=False)
    db.commit()
    return {"isSuccess": True}