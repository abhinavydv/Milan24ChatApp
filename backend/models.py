# models.py
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    picture = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(String)
    phone_number = Column(String)

    contacts = relationship('Contact', back_populates='user', cascade="all, delete-orphan", passive_deletes=True)
    messages_sent = relationship('Message', foreign_keys='Message.from_user_id', back_populates='from_user')
    messages_received = relationship('Message', foreign_keys='Message.to_user_id', back_populates='to_user')

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    contact_id = Column(String, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', foreign_keys=[user_id], back_populates='contacts')
    contact = relationship('User', foreign_keys=[contact_id])

    __table_args__ = (UniqueConstraint('user_id', 'contact_id', name='_user_contact_uc'),)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True)
    from_user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    to_user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    from_user = relationship('User', foreign_keys=[from_user_id], back_populates='messages_sent')
    to_user = relationship('User', foreign_keys=[to_user_id], back_populates='messages_received')
