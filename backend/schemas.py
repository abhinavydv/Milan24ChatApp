# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    id: str
    email: EmailStr
    name: str
    picture: str

    class Config:
        orm_mode = True

class UpdateProfile(BaseModel):
    first_name: str
    last_name: str
    dob: str
    phone_number: str

class AddContact(BaseModel):
    email_id: EmailStr

class MessageCreate(BaseModel):
    to_user_email: EmailStr
    content: str

class MessageResponse(BaseModel):
    id: str
    from_user_id: str
    to_user_id: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

class ContactResponse(BaseModel):
    id: str
    contact: UserBase

    class Config:
        orm_mode = True
