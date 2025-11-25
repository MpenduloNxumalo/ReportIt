from fastapi import FastAPI

from controllers.community_problem_controller import router as community_problem_router
from controllers.location_controller import router as location_router
from controllers.municipality_controller import router as municipality_router
from controllers.user_controller import router as user_router
from databases.report_it_database import engine
from models.report_it_models import *

app = FastAPI()

Base.metadata.create_all(bind=engine)

#--------------------------- API Routers ---------------------------#
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(community_problem_router, prefix="/community_problems", tags=["Community Problems"])
app.include_router(municipality_router, prefix="/municipalities", tags=["Municipalities"])
app.include_router(location_router, prefix="/locations", tags=["Locations"])