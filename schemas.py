from pydantic import BaseModel
from enums.report_it_enums import Status
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class CommunityProblemCreate(BaseModel):
    user_id: int
    municipal_id: int
    location_id: int
    description: str
    date: datetime
    status: Status

class MunicipalityCreate(BaseModel):
    name: str
    phone_number: str
    location_id: int

class LocationCreate(BaseModel):
    latitude: float
    longitude: float