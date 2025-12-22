from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix='/auth', tags=["auth"])

@auth_router.get('/')
async def home():
    """
    Essa é a rota padrão de autenticação
    """
    return{"message":"Você está na rota de autenticação", "auth":False}

@auth_router.post("/create")
async def create_account(user_schema: UserSchema, session: Session=Depends(get_session)):
    user = session.query(User).filter(User.user_schema.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado.")
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, encrypted_password)
        session.add(new_user)
        session.commit()
        return {'message': f'Usuário {user_schema.email} cadastrado com sucesso.'}