from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address>/<hostname>"

#Hardcode
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:%s@localhost/fastapi" % quote_plus("1806@ism")

#from Env
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:%s@{settings.db_hostname}/{settings.db_dbname}" \
                          % quote_plus(settings.db_password)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base Class
Base = declarative_base()

#Create a Session for DB Operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

