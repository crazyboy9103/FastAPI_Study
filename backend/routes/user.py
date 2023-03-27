from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from pydantic import BaseModel
from typing import List
import bcrypt

from models.models import User_Pydantic, User

# 비밀번호 암호화
def encode(text: str) -> str:
    return bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(input_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

class Status(BaseModel):
    message: str
    code: int

class LoginForm(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.get(
    "/users", 
    response_model=List[User_Pydantic]
)
async def get_users():
    return await User_Pydantic.from_queryset(User.all())

@router.post(
    "/users", 
    response_model=User_Pydantic
)
async def create_user(user: User_Pydantic):
    temp = user.dict(exclude_unset=True)
    temp.update({"password": encode(temp["password"])})
    user_obj = await User.create(**temp)
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.post(
    "/check_user", 
    response_model=Status, 
    responses={404: {"model": HTTPNotFoundError}}
)
async def check_user(login_form: LoginForm):
    user_obj = await User_Pydantic.from_queryset_single(User.get(email=login_form.email))
    correct = check_password(login_form.password, user_obj.password)
    if correct:
        return Status(message="Correct", code=0)
    else:
        return Status(message="Wrong", code=1)


@router.get(
    "/user/{user_id}", 
    response_model=User_Pydantic, 
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(user_id=user_id))

@router.delete(
    "/user/{user_id}", 
    response_model=Status, 
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_user(user_id: int):
    deleted_count = await User.filter(user_id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}", code=0)