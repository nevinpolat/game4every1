# initialize_db.py

import os
from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set!")

# Create an engine
engine = create_engine(DATABASE_URL)

# Create all tables in the database
Base.metadata.create_all(engine)

print("Tables created successfully!")

