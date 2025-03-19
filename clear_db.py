from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.db.database import Base
from app.core.config import settings

DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

def clear_database():
    Base.metadata.drop_all(bind=create_engine(DATABASE_URL))
    print("Database has been cleared.")

if __name__ == "__main__":
    clear_database()
