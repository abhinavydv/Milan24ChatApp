from fastapi import APIRouter, Depends, Response, Cookie
from fastapi import UploadFile,File
from sqlalchemy import update,or_,and_
from sqlalchemy.orm import Session

from config.db import get_db
from schemas.message import Message

router = APIRouter(
    prefix="/message",
    tags=["Message"],
)

@router.websocket("/ws")
def websocket_endpoint():
    pass
