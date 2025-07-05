from fastapi import APIRouter, status, HTTPException
from app.db.database import SessionDep
from app.models.models import User
from sqlmodel import select
from app.core.security import hash_password,verify_password
from app.core.security import create_access_token
from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Response, status

from app.schemas.user import RegisterUser, UserResponse, LoginResponse,LoginUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#  router 
router = APIRouter(prefix="/api", tags=["authentication"])




@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(req: RegisterUser, db: SessionDep):
    if db.exec(select(User).where(User.email == req.email)).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = hash_password(req.password)

    user = User(
        username=req.username,
        email=req.email,
        role=req.role,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user  # Automatically serialized using UserResponse

@router.post("/login", response_model=LoginResponse)
async def login_user(req: LoginUser, db: SessionDep, response: Response):
    user = db.exec(select(User).where(User.email == req.email)).first()
    if not user or not user.password_hash or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(user.id)})

    # ✅ Set JWT as HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,  # 30 minutes
        secure=True,
        samesite="lax"
    )

    return {"username": user.username,"email":user.email, "access_token": access_token}
#  logout

from fastapi import Response

@router.get("/logout", status_code=200)
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
