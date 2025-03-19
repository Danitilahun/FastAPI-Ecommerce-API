import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.database import get_db, Base
from fastapi.testclient import TestClient
from app.main import app

TEST_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def override_get_db():
    """Override the get_db dependency to use the testing session."""
    def get_db_override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    return get_db_override


@pytest.fixture(scope="module")
def test_app(override_get_db):
    """Set up the FastAPI app with overridden DB session for testing."""
    app.dependency_overrides[get_db] = override_get_db
    yield app 

@pytest.fixture()
def test_db(test_app):
    """Provide a fresh database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(test_app):
    """Provide a TestClient instance for sending requests to the FastAPI app."""
    return TestClient(test_app)
