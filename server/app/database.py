import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/chatdb")

# Create an engine with a connection pool
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)

######################
# TODO: use alembic for schema changes/migrations
# Create tables
Base.metadata.create_all(engine)
######################

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


