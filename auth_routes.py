from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix='/auth', tags=["auth"])

def create_token(user_id):
    token = f'hubef2490fji{user_id}'
    return token

@auth_router.get('/')
async def home():
    """
    Essa é a rota padrão de autenticação
    """
    return{"message":"Você está na rota de autenticação", "auth":False}

@auth_router.post("/create")
async def create_account(user_schema: UserSchema, session: Session=Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado.")
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, encrypted_password)
        session.add(new_user)
        session.commit()
        return {'message': f'Usuário {user_schema.email} cadastrado com sucesso.'}

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==login_schema.email).first()
    if not user:
        raise HTTPException(status_code=500, detail='Usuário não encontrado')
    else:
        acess_token = create_token(user.id)
        return {
            "acess_token": acess_token,
            "token_type": "Bearer"
        }