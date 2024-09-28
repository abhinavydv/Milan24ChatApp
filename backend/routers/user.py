# routers/user.py
from fastapi import APIRouter, Depends, HTTPException, Header
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from uuid import uuid4
from models import User as UserModel, Contact as ContactModel
from schemas import UpdateProfile, AddContact, UserBase, ContactResponse
from utils.auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from config.db import get_db
import os

router = APIRouter(prefix="/user", tags=["User"])
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

@router.post("/login", response_model=dict)
async def login(authorization: str = Header(None), db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(
            authorization, requests.Request(), audience=GOOGLE_CLIENT_ID
        )
        email = idinfo["email"]
        name = idinfo["name"]
        picture = idinfo.get("picture", "")
        user_id = idinfo["sub"]

        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            user = UserModel(id=user_id, email=email, name=name, picture=picture)
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token")

@router.put("/profile", response_model=UserBase)
def update_profile(
    profile_data: UpdateProfile,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for key, value in profile_data.dict().items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/add_contact", response_model=dict)
def add_contact(
    contact_data: AddContact,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contact = db.query(UserModel).filter(UserModel.email == contact_data.email_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if contact.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot add yourself as a contact")
    existing_contact = db.query(ContactModel).filter_by(
        user_id=current_user.id, contact_id=contact.id
    ).first()
    if existing_contact:
        raise HTTPException(status_code=400, detail="Contact already added")
    new_contact = ContactModel(
        id=uuid4().hex, user_id=current_user.id, contact_id=contact.id
    )
    db.add(new_contact)
    db.commit()
    return {"message": "Contact added"}

@router.get("/contacts", response_model=List[ContactResponse])
def get_contacts(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contacts = db.query(ContactModel).filter(ContactModel.user_id == current_user.id).all()
    return contacts
