from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from datetime import date
from uuid import uuid4
import os
from sqlmodel import select
from app.db.database import SessionDep
from app.models.models import Customer
from app.schemas.customer import CustomerResponse

router = APIRouter(prefix="/customer", tags=["Customer"])
os.makedirs("static/images", exist_ok=True)

@router.post("/open", status_code=201, response_model=CustomerResponse)
async def create_customer(
    db: SessionDep,
    user_id: int = Form(...),
    name: str = Form(...),
    dob: date = Form(...),
    phone_no: str = Form(...),
    address: str = Form(...),
    aadhar_card: str = Form(...),
    kyc_verified: bool = Form(...),
    file: UploadFile = File(...)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files allowed.")
    
    if not file.filename:
        raise HTTPException(400, "Uploaded file must have a filename.")
    image_ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else ''
    image_name = f"{uuid4()}.{image_ext}" if image_ext else f"{uuid4()}"
    path = f"static/images/{image_name}"
    with open(path, "wb") as f:
        f.write(await file.read())

    if db.exec(select(Customer).where(Customer.user_id == user_id)).first():
        raise HTTPException(400, "Customer already exists.")
    if db.exec(select(Customer).where(Customer.aadhar_card == aadhar_card)).first():
        raise HTTPException(400, "Aadhar already exists.")

    customer = Customer(
        user_id=user_id, photo=f"/{path}", name=name, dob=dob,
        phone_no=phone_no, address=address, aadhar_card=aadhar_card,
        kyc_verified=kyc_verified
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer
