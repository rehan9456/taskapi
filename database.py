from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = (
    "mssql+pyodbc://@DESKTOP-OVJ6V3Q/task_manager_db"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL)

sessionlocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()




                       

