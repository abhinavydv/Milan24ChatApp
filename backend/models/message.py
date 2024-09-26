from pydantic import BaseModel


class Message(BaseModel):
    to_user: str
    message: str

class MessageId(BaseModel):
    id: str

