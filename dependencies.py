from models import db
from sqlalchemy.orm import sessionmaker

def get_session():
    try:
        Session = sessionmaker(bind=db) #conexão
        session = Session() #instância
        yield session
    finally:
        session.close()