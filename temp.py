import os

structure = {
    "app": {
        "__init__.py": "",
        "main.py": """
from fastapi import FastAPI
from app.routes import router as main_router

app = FastAPI(title="My FastAPI App")

app.include_router(main_router)
""",
        "core": {
            "__init__.py": "",
            "config.py": """
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
"""
        },
        "routes": {
            "__init__.py": """
from fastapi import APIRouter
from .user import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["Users"])
""",
            "user.py": """
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_users():
    return [{"id": 1, "name": "Alice"}]
"""
        },
        "db": {
            "__init__.py": "",
            "session.py": """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
""",
            "models.py": """
from sqlalchemy import Column, Integer, String
from .session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
"""
        },
        "utils": {
            "__init__.py": "",
            "hash.py": """
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
"""
        },
    },
    ".env": "DATABASE_URL=sqlite:///./test.db",
    "requirements.txt": """fastapi
uvicorn[standard]
sqlalchemy
pydantic
passlib[bcrypt]
python-dotenv""",
    "run.py": """
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
"""
}

def create_structure(base_path, structure_dict):
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

if __name__ == "__main__":
    create_structure(".", structure)
    print("✅ FastAPI project (with top-level 'app/') created successfully!")
