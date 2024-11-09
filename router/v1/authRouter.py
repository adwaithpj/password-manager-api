from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from schemas.pydantic.authSchema import (
    TokenSchema,
    TokenDataSchema,
)
from schemas.pydantic.UserSchema import (
    UserLoginSchema,
)
from services.AuthService import AuthService
from starlette import status
from configs.Database import SessionLocal
from models.Userdb import User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


AuthRouter = APIRouter(prefix="/v1/auth", tags=["auth"])


@AuthRouter.post("/token", status_code=200, response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authService: AuthService = Depends(),
):
    token_data = authService.login(form_data.username, form_data.password)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return token_data
