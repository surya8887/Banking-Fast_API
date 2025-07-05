from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.customer import router as customer_router
from app.db.database import create_db_and_tables  # Make sure this exists
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Banking API",
    description="API for banking operations",
    version="0.1.0",
)


app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Run this when FastAPI starts
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/')
async def root():
    return {"message": "Hello World"}

app.include_router(user_router)
app.include_router(customer_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
