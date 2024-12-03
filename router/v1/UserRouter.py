from typing import List, Optional, Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from schemas.pydantic.UserSchema import (
    UserCreateSchema,
    UserBaseSchema,
    UserGetSchema,
    UserPatchSchema,
)
from services.UserService import UserService
from services.AuthService import AuthService
from starlette import status

UserRouter = APIRouter(prefix="/v1/users", tags=["user"])

authservice = AuthService()
user_dependency = Annotated[dict, Depends(authservice.get_current_user)]


@UserRouter.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=UserGetSchema
)
def create_user(user: UserCreateSchema, userService: UserService = Depends()):
    return userService.create(user).normalize()


@UserRouter.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserGetSchema)
async def get_users_by_id(
    id: int, user: user_dependency, userService: UserService = Depends()
):
    if user.id != id and user.id != 5:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to access this user",
        )
    get_user = userService.get(id)
    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return get_user


@UserRouter.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(
    id: int,
    user: user_dependency,
    userService: UserService = Depends(),
):
    if id == user.id:
        result = userService.delete(id)
        if result:
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    elif id == 5:
        return {"Caution": "Admin User"}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to delete this user",
        )


@UserRouter.patch("/{id}", status_code=status.HTTP_200_OK, response_model=UserGetSchema)
async def update_user(
    id: int,
    user_patch: UserPatchSchema,
    user: user_dependency,
    userService: UserService = Depends(),
):
    if user.id != id and user.id != 5:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Use 403 for unauthorized access
            detail="Not authorized to update this user.",
        )

    updated_user = userService.update(id, user_patch)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return updated_user
