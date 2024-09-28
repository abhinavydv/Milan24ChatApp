from fastapi import APIRouter, Depends, Response, Cookie
from fastapi import UploadFile,File
from sqlalchemy import update,or_,and_
from sqlalchemy.orm import Session
from utils.util import verify_auth_token

from config.db import get_db
from schemas.user import User
from models.user import GoogleLogin

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.get("/get_user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    # user = db.query(User).filter(User.id == user_id).first()
    user = {"id": 1, "first_name": "John", "last_name": "Doe", "dob": "01-01-2000"}
    return user

@router.get("/login")
def handle_login(details: dict = Depends(verify_auth_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email_id == details["email"]).first() 
    if user is None:
        user = User(email_id=details["email"], first_name=details["fname"],last_name=details["lname"])
        db.add(user)
        db.commit()
        return {"message":"Sign Up Successful"}
    else:
        return {"message":"Login Successful"}