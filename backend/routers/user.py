from fastapi import APIRouter, Depends, Response, Cookie
from fastapi import UploadFile,File
from sqlalchemy import update,or_,and_
from sqlalchemy.orm import Session

from config.db import get_db
from schemas.user import User
from models.user import GoogleLogin

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.post("/google_login")
def google_login(loginInfo: GoogleLogin):
    print("google_login", loginInfo)
    pass

@router.get("/get_user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    # user = db.query(User).filter(User.id == user_id).first()
    user = {"id": 1, "first_name": "John", "last_name": "Doe", "dob": "01-01-2000"}
    return user
