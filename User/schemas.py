#Schemas basically defines what to takes from user.
#Basically,Response model means not related to DB but pydantic, schemas.

from tokenize import String
from pydantic import BaseModel
from sqlalchemy import true

class AdminUser(BaseModel): #Table
    name: str               #Field
    email: str
    password: str
    verify_password: str
    blood_group: str
    is_active: bool
    class Config():
        orm_mode = True

class WeightTargetGoals(BaseModel):
    user_id: int
    targetWeight: int
    targetTimeFrame: str
    class Config():
        orm_mode = True

#We can give the ShowAdminUser to main.py response_model= inorder to display only name and email after post.
class ShowBloodMates(BaseModel):
    name: str
    email:str
    is_active: bool
    blood_group: str
    class Config():
        orm_mode = True
class ShowAdminUser(BaseModel):
    id: int
    name: str
    email:str
    blood_group: str
    is_active: bool
    class Config():
        orm_mode = True
