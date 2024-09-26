from pydantic import BaseModel

class GoogleLogin(BaseModel):
    email: str
    name: str
    picture: str
    google_id: str

class UpdateProfile(BaseModel):
    first_name: str
    last_name: str
    dob: str
    phone_number: str

class AddContact(BaseModel):
    email_id: str


