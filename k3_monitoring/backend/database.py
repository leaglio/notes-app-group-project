from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

import os

# Get the absolute path to the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# The database will be stored in the 'data' folder relative to the project root
DB_PATH = os.path.join(BASE_DIR, "..", "data", "k3_compliance.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    worker_id = Column(String)
    ppe_type = Column(String)  # Helmet, Vest, etc.
    status = Column(String)    # 'Missing' or 'Incorrect'
    image_path = Column(String)
    is_resolved = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)
