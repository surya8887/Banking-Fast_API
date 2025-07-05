# Banking API

A FastAPI-based API for banking operations, providing endpoints for user and customer management, with database integration and static file serving.

## Features

- User and Customer API routes
- Database setup and migrations with SQLAlchemy and Alembic
- Password hashing and JWT authentication support
- Background tasks with Celery
- Caching with Redis
- Static file serving
- API documentation with OpenAPI (Swagger UI)
- Async database operations with asyncpg and SQLModel

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Banking Fast_API
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the FastAPI app using the provided run.py script:

```bash
python run.py
```

Alternatively, run with uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /` - Root endpoint returning a welcome message.
- User routes - defined in `app/routes/user.py`
- Customer routes - defined in `app/routes/customer.py`
- Static files served at `/static`

API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

Key dependencies include:

- FastAPI
- Uvicorn
- SQLAlchemy, asyncpg, Alembic
- Pydantic
- Passlib (for password hashing)
- Python-JOSE (for JWT)
- Redis and aioredis
- Celery and Flower
- Loguru
- APScheduler
- SQLModel
- Testing tools: pytest, pytest-asyncio, mypy, black, isort, flake8, coverage

## Contributing

Contributions are welcome. Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.
