import string
#Models basically designs the Tables in the SQLITE.
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
import datetime
from .database import Base


class AdminUsers(Base):
    __tablename__ = "AdminUsers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    password = Column(String)
    verify_password = Column(String)
    blood_group = Column(String)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

class WeightTargetGoals(Base):
    __tablename__ = "WeightTargetGoals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    targetWeight = Column(Integer)
    targetTimeFrame = Column(String)
