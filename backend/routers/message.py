# routers/message.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from models import Message as MessageModel, User as UserModel
from schemas import MessageCreate, MessageResponse
from config.db import get_db
from utils.util import get_current_user
from typing import List
from datetime import datetime

router = APIRouter(prefix="/message", tags=["Message"])

@router.post("/send", response_model=MessageResponse)
def send_message(
    message_data: MessageCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    to_user = db.query(UserModel).filter(UserModel.email == message_data.to_user_email).first()
    if not to_user:
        raise HTTPException(status_code=404, detail="Recipient not found")
    new_message = MessageModel(
        id=uuid4().hex,
        from_user_id=current_user.id,
        to_user_id=to_user.id,
        content=message_data.content,
        timestamp=datetime.utcnow()
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/conversation/{contact_id}", response_model=List[MessageResponse])
def get_conversation(
    contact_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    messages = (
        db.query(MessageModel)
        .filter(
            ((MessageModel.from_user_id == current_user.id) & (MessageModel.to_user_id == contact_id)) |
            ((MessageModel.from_user_id == contact_id) & (MessageModel.to_user_id == current_user.id))
        )
        .order_by(MessageModel.timestamp)
        .all()
    )
    return messages
