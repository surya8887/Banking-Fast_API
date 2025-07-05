from pydantic import BaseModel
from datetime import date

class NewCustomer(BaseModel):
    user_id: int
    photo_url: str  # URL to uploaded image
    name: str
    dob: date
    phone_no: str
    address: str
    aadhar_card: str
    kyc_verified: bool


# Response schema (optional)
class CustomerResponse(BaseModel):
    user_id: int
    photo: str
    name: str
    dob: date
    phone_no: str
    address: str
    aadhar_card: str
    kyc_verified: bool

    class Config:
        from_attributes = True
