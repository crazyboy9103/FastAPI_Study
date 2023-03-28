# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

# Pydantic Model로부터 schema, serialization 둘다 할수 있음
# from tortoise.contrib.pydantic import pydantic_model_creator
# Tournament_Pydantic = pydantic_model_creator(Tournament)
# print(Tournament_Pydantic.schema())
# tournament = await Tournament.create(name="New Tournament")
# tourpy = await Tournament_Pydantic.from_tortoise_orm(tournament)
# >>> print(tourpy.dict())
# {
#     'id': 1,
#     'name': 'New Tournament',
#     'created_at': datetime.datetime(2020, 3, 1, 20, 28, 9, 346808)
# }
# >>> print(tourpy.json())
# {
#     "id": 1,
#     "name": "New Tournament",
#     "created_at": "2020-03-01T20:28:09.346808"
# }


# Model 클래스로부터 쿼리를 시작할 수 있음
# e.g. 
#   User.filter(*args, **kwargs)
#   User.exclude(*args, **kwargs)
#   User.all()
#   User.first()
#   User.annotate()

# 이렇게 치면 QuerySet 이라는 객체를 만드는데, 더 다양한 필터링이나 계산에 사용됨

#   User.create(**kwargs) : **kwargs로 부터 User 객체를 생성함
#   User.get_or_create(defaults, **kwargs) : 
#      **kwargs로부터 받은 값으로 객체를 찾고 있으면 가져오고, 없으면 defaults에서 나머지 빈 필드에
#       채워넣고 생성함 

#   User.save() : 인스턴스 업데이트, 저장
#   User.delete() : 인스턴스 삭제
#   User.fetch_related(*args) : 
#       e.g. await team.fetch_related('events__tournament')
#            team과 FK로 엮여있는 events를 모두 가져오고, 각 event와 엮여있는 tournament도 가져옴
# 

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, validator
from typing import Annotated, List
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET  = "fb526cd12314a1bcc35ebaa2c3c85f6141d97ae0360e65345a3b92291067238c"
JWT_ALGORITHM  = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 30


from models.models import User_Pydantic, User
from models.auth_models import AuthUser_Pydantic, AuthUser
from models.logs import LoginLog_Pydantic, LoginLog


# 비밀번호를 str으로 hash하기 위한 함수
def hash_password(password: str) -> str:
    return password_context.hash(password)

# hash된 비밀번호를 검증
def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

# expires_delta 분 후에 만료되는 jwt를 만든다
def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

class Token(BaseModel):
    access_token: str
    refresh_token: str
    message: str

class RefreshToken(BaseModel):
    refresh_token: str


class LoginForm(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def password_validator(cls, v):
        if len(v) < 6:
            raise ValueError('비밀번호는 최소 6자리')
        return v
    
class Response(BaseModel):
    code: int
    message: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/token") #

router = APIRouter(
    prefix="/auth",
    tags = ["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

import logging
logger = logging.getLogger("uvicorn")


@router.post(
    "/users",
    response_model=Response
)
async def create_user(user: AuthUser_Pydantic):
    temp = user.dict(exclude_unset=True)
    temp.update({"password": hash_password(temp["password"])})
    user_obj = await AuthUser.create(**temp)
    await AuthUser_Pydantic.from_tortoise_orm(user_obj)
    res = Response(code=0, message="Success")
    return res


async def authenticate_user(email: str, password: str) -> AuthUser:
    user = await AuthUser.get_or_none(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No such email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def create_loginlog(user: AuthUser):
    log = {"user_id": user.user_id}
    login_log = await LoginLog.create(**log)
    await LoginLog_Pydantic.from_tortoise_orm(login_log)

@router.post(
    "/login",
    response_model=Token
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # OAuth2PasswordRequestForm requires username, password parameters wrapped in FormData
    user = await authenticate_user(
        email=form_data.username, 
        password=form_data.password
    )
    if user:
        await create_loginlog(user)

    access_token = create_access_token(
        data = {"sub": user.email}, 
        expires_delta = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_access_token(
        data = {"sub": user.email}, 
        expires_delta = JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 # days * 24 * 60 = minutes
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "message": "성공"}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthUser:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        
        if payload.get("exp") < int(datetime.utcnow().timestamp()):
            raise HTTPException(status_code=400, detail="Expired token")

        user = await AuthUser.get_or_none(email=email)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid email")
        
        return user
    
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
@router.get(
    "/me",
    response_model=AuthUser_Pydantic
)
async def get_me(
    current_user: Annotated[AuthUser, Depends(get_current_user)] # Depends(get_current_user) /me 에 요청을 보내면
                                                                 # get_current_user를 실행시킨 결과를 current_user로 사용하여 함수 실행 
):
    return current_user

@router.post(
    "/new_token"
)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        
        if payload.get("exp") < int(datetime.utcnow().timestamp()):
            # raise HTTPException(status_code=400, detail="Expired refresh token")
            pass

        user = await AuthUser.get_or_none(email=email)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid email")
        
        access_token = await create_access_token(
            data = {"sub": user.email}, 
            expires_delta = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token = await create_access_token(
            data = {"sub": user.email}, 
            expires_delta = JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 # days * 24 * 60 = minutes
        )
        return {"access_token": access_token, "refresh_token": refresh_token, "message": "성공"}
    
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    
@router.get(
    "/me/loginLogs",
    response_model=List[LoginLog_Pydantic]
)
async def get_my_login_logs(
    current_user: Annotated[AuthUser, Depends(get_current_user)] # Depends(get_current_user) /me 에 요청을 보내면
                                                                 # get_current_user를 실행시킨 결과를 current_user로 사용하여 함수 실행 
):
    return await current_user.login_logs