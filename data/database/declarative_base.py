import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Retrieve the database connection information from environment variables
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
database = os.getenv('DB_NAME')

# Construct the SQLAlchemy database URI based on the connection information
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(SQLALCHEMY_DATABASE_URI) # Create a session class using the engine
Session = sessionmaker(bind=engine)
Base = declarative_base()# Create the base class for declarative models
