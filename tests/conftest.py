import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.database import get_db, Base
from fastapi.testclient import TestClient  # Import TestClient
from app.main import app  # Import your FastAPI app

# Override the database URL for testing using the same development URL.
TEST_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

# Create the test database engine
engine = create_engine(TEST_DATABASE_URL)

# Create a configured "Session" class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a fixture to override get_db for testing (module scoped)
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

# Fixture to provide the FastAPI app with overridden DB session for testing (module scoped)
@pytest.fixture(scope="module")
def test_app(override_get_db):
    """Set up the FastAPI app with overridden DB session for testing."""
    app.dependency_overrides[get_db] = override_get_db  # Override the DB dependency
    yield app  # Return the FastAPI app for testing
    # Optionally, you could add code to tear down here (e.g., dropping tables or rolling back transactions)

# Fixture to provide a fresh database session for each test (function scoped)
@pytest.fixture()
def test_db(test_app):
    """Provide a fresh database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture to provide a TestClient for FastAPI app (function scoped)
@pytest.fixture()
def client(test_app):
    """Provide a TestClient instance for sending requests to the FastAPI app."""
    return TestClient(test_app)
