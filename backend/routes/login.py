from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel

class User(BaseModel):
    name: str

router = APIRouter()

@router.post(
    "/login"
)
async def login(user: User):
    return user