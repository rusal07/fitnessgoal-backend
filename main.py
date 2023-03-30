from concurrent.futures import process
from pickle import TRUE
from fastapi import FastAPI, Depends, status, HTTPException
#Database settings import.
#The User is the directory and schemas and models are Python file.
from User import schemas, models
from User.database import engine,SessionLocal
from sqlalchemy.orm import Session
from User.inputvalidation import InputValidation
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import List

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500/",
    "http://localhost:3000",
    "https://fitnessgoal.onrender.com",
    "http://fitnessgoal.onrender.com/",
    "https://fitnessgoalbackend.onrender.com/",
    "https://fitnessgoalbackend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""The below code is going to create all models into the database. 
If the table is already there it won't 
going to create a new one else creates."""
models.Base.metadata.create_all(engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#The post request inorder to register an account.

""" We can also define response model, what to show after the successfull post
    @app.post("/api/post", response_model = schemas.Showmodel #But we have to define new showmodel with what
    we only want to show as a response.)
"""
@app.post("/api/registeraccount")
#To connect with Database,we must use, db: Session * )
def create_adminuser(request : schemas.AdminUser, db : Session = Depends(get_db)):
    #Some sort of validations in the input.
    if not ((InputValidation.password_validation(request.password, request.verify_password))):
        return {"Error ": "Password may didn't match & Password length should be greater than 3."}
    if not ((InputValidation.email_validation(request.email))):
        return {"Error": "Email account not valid, Email must consists of @something.com"}
    
    new_adminuser = models.AdminUsers(
        name = request.name,
        email = request.email,
        password = request.password,
        verify_password = request.verify_password,
        blood_group = request.blood_group

        )
    db.add(new_adminuser)
    db.commit()
    db.refresh(new_adminuser)
    return new_adminuser

@app.post("/api/targetgoals")
def set_target_weight(request : schemas.WeightTargetGoals, db : Session = Depends(get_db)):
    new_target = models.WeightTargetGoals(
        user_id = request.user_id,
        targetWeight = request.targetWeight,
        targetTimeFrame = request.targetTimeFrame
        )
    db.add(new_target)
    db.commit()
    db.refresh(new_target)
    return new_target


#Let's fetch the usr by their ID
@app.get("/api/user/{id}", response_model=schemas.ShowAdminUser)
def show_response(id: int, db=Depends(get_db)):
    user = db.query(models.AdminUsers).filter(models.AdminUsers.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found.")
    return user

@app.get("/api/bloodmates/{id}", response_model=List[schemas.ShowBloodMates])
def show_response(id: int, db=Depends(get_db)):
    user = db.query(models.AdminUsers).filter(models.AdminUsers.id != id).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found.")
    return user

#GoalsUserCheck
@app.get("/api/targetuser/{id}")
def show_response(id: int, db=Depends(get_db)):
    user = db.query(models.WeightTargetGoals).filter(models.WeightTargetGoals.user_id == id).first()
    if not user:
        print("Not found")
    return user

@app.get("/api/user")
def show_response( db=Depends(get_db)):
   user = db.query(models.AdminUsers).all()
   return user

@app.get("/api/loginuser/{email}/{password}")
def show_response(email: str, password: str, db=Depends(get_db)):
    user = db.query(models.AdminUsers).filter(models.AdminUsers.email == email , models.AdminUsers.password == password).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with Email {email} not found.")
    return user

