from typing import List, Optional, Annotated, Dict
from fastapi import APIRouter, Depends, status, HTTPException

from schemas.pydantic.UserSchema import UserGetSchema
from schemas.pydantic.PasswordSchema import (
    PasswordGetSchema,
    PasswordCreateSchema,
    PasswordUpdateSchema,
)
from services.UserService import UserService
from services.AuthService import AuthService
from services.PasswordService import PasswordService
from starlette import status

PasswordRouter = APIRouter(prefix="/v1/pass", tags=["password"])

authService = AuthService()
user_dependency = Annotated[dict, Depends(authService.get_current_user)]


@PasswordRouter.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=PasswordGetSchema,
)
async def create(
    password: PasswordCreateSchema,
    user: user_dependency,
    passwordService: PasswordService = Depends(),
):
    if not user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to access this user",
        )
    return passwordService.create(
        id=user.id, passwordData=password, pass_key=user.pass_key
    )


# Update the password entries
@PasswordRouter.patch(
    "/{id}/update",
    status_code=status.HTTP_200_OK,
    response_model=PasswordGetSchema,
)
async def update(
    id: int,
    password: PasswordUpdateSchema,
    user: user_dependency,
    passwordService: PasswordService = Depends(),
):

    return passwordService.update(
        id=id, user_id=user.id, passwordData=password, pass_key=user.pass_key
    )


# get password of user from its password id.
@PasswordRouter.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=PasswordGetSchema,
)
async def get(
    id: int, user: user_dependency, passwordService: PasswordService = Depends()
):
    return passwordService.get(id, user.id, user.pass_key)


# Get all the password attached to a user
@PasswordRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[PasswordGetSchema],
)
async def index(
    user: user_dependency,
    pageSize: Optional[int] = 100,
    startindex: Optional[int] = 0,
    passwordService: PasswordService = Depends(),
):
    password = [
        password
        for password in passwordService.list(
            user.id, user.pass_key, pageSize, startindex
        )
    ]
    return password


# Delete password entries of current user only
@PasswordRouter.delete("/delete/{id}", status_code=200, response_model=Dict)
async def delete(
    id: int,
    user: user_dependency,
    passwordService: PasswordService = Depends(),
):
    if passwordService.delete(id, user.id):
        return {"success": "Password was successfully deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password was not found/deleted",
        )
