from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
import schemas
from models.report_it_models import *
from databases.report_it_database import engine, SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = UserModel(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user


