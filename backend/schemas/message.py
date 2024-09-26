from config import db
from sqlalchemy import Column, Integer, String, Text, Boolean


class Message(db.Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(Integer, unique=True)
    to_user = Column(String)
    message = Column(Text)
    delivered = Column(Boolean)
    read = Column(Boolean)
    deleted = Column(Boolean)
    created_ts = Column(String)
    updated_ts = Column(String)
    deleted_by = Column(Integer)
    deleted_ts = Column(String)
