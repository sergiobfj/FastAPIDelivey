from config import ALGORITHM, SECRET_KEY, oauth2_schema
from sqlalchemy.orm import Session
from models import User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from database import SessionLocal


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def verify_user(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    user = session.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user
