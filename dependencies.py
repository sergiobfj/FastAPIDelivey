from main import ALGORITHM, SECRET_KEY, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError



def get_session():
    try:
        Session = sessionmaker(bind=db) #conexão
        session = Session() #instância
        yield session
    finally:
        session.close()

def verify_user(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dict_info.get("sub"))
    except JWTError as error:
        print(error)
        raise HTTPException(status_code=401, detail="Acesso negado")
    user = session.query(User).filter(User.id==user_id).first
    if not user:
        raise HTTPException(status_code=401, detail="Acesso negado")

    return user
