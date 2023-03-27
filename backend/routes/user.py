from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from pydantic import BaseModel
from typing import List

from models.models import User_Pydantic, User


class Status(BaseModel):
    message: str

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
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.get(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
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
    return Status(message=f"Deleted user {user_id}")