from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session, verify_user
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix='/auth', tags=["auth"])

def create_token(user_id, time_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE)):
    data_expire = datetime.now(timezone.utc) + time_token
    info_dict = {"sub": str(user_id), "exp": data_expire}
    encoded_jwt = jwt.encode(info_dict, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def auth_user(email, password, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user



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
    
@auth_router.post('/login-form')
async def login_form(forms_data: OAuth2PasswordRequestForm = Depends(),session: Session = Depends(get_session)):
    user = auth_user(forms_data.username, forms_data.password, session)
    if not user:
        raise HTTPException(status_code=500, detail='Usuário não encontrado ou credenciais inválidas')
    else:
        acess_token = create_token(user.id)
        return {
            "acess_token": acess_token,    
            "token_type": "Bearer"
        }

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = auth_user(login_schema.email, login_schema.password,session)
    if not user:
        raise HTTPException(status_code=500, detail='Usuário não encontrado ou credenciais inválidas')
    else:
        acess_token = create_token(user.id)
        refresh_token = create_token(user.id, time_token=timedelta(days=7))
        return {
            "acess_token": acess_token,
            "refresh_token": refresh_token,     
            "token_type": "Bearer"
        }
    
@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verify_user)):
    acess_token = create_token(user.id)
    return{
        "acess_token": acess_token,  
        "token_type": "Bearer"
    }

