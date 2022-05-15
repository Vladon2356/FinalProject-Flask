from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import BaseConfig

db = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
base = declarative_base()
Session = sessionmaker(db)
session = Session()
