from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Database setup using SQLAlchemy with settings from the configuration file
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)

# Sessionmaker is configured for database interactions.
# bind=engine connects it to the database engine, while autoflush and autocommit are set to False for better control over transactions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
