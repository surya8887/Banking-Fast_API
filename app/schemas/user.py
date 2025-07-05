from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.models import UserRoleEnum


#  Register User
class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRoleEnum

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRoleEnum
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True  # Pydantic v2 compatibility



# Login User 
class LoginUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    username:str
    email: str
    access_token: str

    class Config:
        from_attributes = True  # Pydantic v2 compatibility


