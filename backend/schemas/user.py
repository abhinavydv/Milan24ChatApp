from config import db
from sqlalchemy import Column, Integer, String


class User(db.Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(String)
    phone_number = Column(String)
    gender = Column(String)
