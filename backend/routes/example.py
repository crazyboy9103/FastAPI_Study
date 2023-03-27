from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.get(
    "/example"
)
async def test():
    return {"message": "test"}