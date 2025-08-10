import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Read the database URL from the environment variable
# It will be "postgresql://user:password@db:5432/bank_applications_db" in Docker
# You can also set a default for local development (e.g., SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bank_applications.db")

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class AccountApplication(Base):
    __tablename__ = 'account_applications'
    
    id = Column(Integer, primary_key=True)
    full_name = Column(Text, nullable=False)
    account_type = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    id_number = Column(Text, nullable=False)
    contact = Column(Text, nullable=False, unique=True, index=True)
    status = Column(Text, default='Submitted')
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    # This will create the table when the app starts
    Base.metadata.create_all(engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_user_data(user_data):
    # ... (the rest of the function remains the same)
    db = SessionLocal()
    try:
        new_application = AccountApplication(
            full_name=user_data['name'],
            account_type=user_data['account_type'],
            address=user_data['address'],
            id_number=user_data['id'],
            contact=user_data['contact']
        )
        db.add(new_application)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error saving data: {e}")
        return False
    finally:
        db.close()

def is_duplicate_contact(contact_info):
    # ... (the rest of the function remains the same)
    db = SessionLocal()
    try:
        existing_application = db.query(AccountApplication).filter_by(contact=contact_info).first()
        return existing_application is not None
    finally:
        db.close()