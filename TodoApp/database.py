# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL='postgresql://postgres:vish26@localhost/TodoApplicationDatabase'

# engine=create_engine(SQLALCHEMY_DATABASE_URL)
                     
# SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base=declarative_base()


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Automatically looks for Render's cloud URL variable first. 
# If it doesn't find it (like when you are working locally), it uses your local computer fallback string.
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:vish26@localhost/TodoApplicationDatabase"
)

# 2. Render cloud database paths start with 'postgres://', 
# but SQLAlchemy 2.0 strictly requires 'postgresql://'. This line automatically fixes it.
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
