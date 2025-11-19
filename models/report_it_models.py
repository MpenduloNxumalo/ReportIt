from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from databases.report_it_database import Base
from enums.report_it_enums import Status


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    problems = relationship("CommunityProblemModel", back_populates="reported_by")


class CommunityProblemModel(Base):
    __tablename__ = 'community_problem'

    community_problem_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    municipal_id = Column(Integer, ForeignKey('municipality.municipal_id'))
    location_id = Column(Integer, ForeignKey('location.location_id'))
    description = Column(String)
    date = Column(DateTime)
    status = Column(Enum(Status), default=Status.PENDING)

    reported_by = relationship("UserModel", back_populates="problems")
    municipality = relationship("MunicipalityModel")
    location = relationship("LocationModel")


class MunicipalityModel(Base):
    __tablename__ = 'municipality'

    municipal_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    location_id = Column(Integer, ForeignKey('location.location_id'))

    community_problems = relationship("CommunityProblemModel", back_populates="municipality")


class LocationModel(Base):
    __tablename__ = 'location'

    location_id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)

    problems = relationship("CommunityProblemModel", back_populates="location")
