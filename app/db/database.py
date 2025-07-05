from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy import text


# Define the database URL
DB_NAME = "Banking"
sqlite_URL = f"sqlite:///{DB_NAME}.db"

# Define the database engine
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_URL, connect_args=connect_args)

# Create database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency for session
def get_session():
    with Session(engine) as session:
        yield session

# Annotated dependency for FastAPI
SessionDep = Annotated[Session, Depends(get_session)]

# Connection check function
def connection_check():
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))  # ✅ Correct usage
            return True
    except Exception as e:
        print(f"Connection Error: {e}")
        return False
    


connection_check()