from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, status, HTTPException

from schemas.pydantic.UserSchema import UserGetSchema
from schemas.pydantic.PasswordSchema import PasswordGetSchema
from services.UserService import UserService
from services.AuthService import AuthService
from services.PasswordService import PasswordService
from starlette import status

PasswordRouter = APIRouter(prefix="/v1/user/", tags=["password"])

authService = AuthService()
user_dependency = Annotated[dict, Depends(authservice.get_current_user)]


@PasswordRouter.post("{id}/pass/create",status_code=status.HTTP_201_CREATED,response_model)