from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
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

authService = AuthService()
user_dependency = Annotated[dict, Depends(authService.get_current_user)]


@AuthRouter.post("/token", status_code=200, response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    authService: AuthService = Depends(),
):
    token_data = authService.login(form_data.username, form_data.password, response)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return token_data


@AuthRouter.post("/login", status_code=200)
async def login(user: user_dependency, response: JSONResponse):
    if user:
        return {"Success": True, "userid": user.id}
    else:
        raise HTTPException(status_code=401, detail="Not authorized")


@AuthRouter.post("/logout", status_code=status.HTTP_200_OK)
async def logout(user: user_dependency, response: JSONResponse):
    if user:
        response.delete_cookie(key="access_token")
        return {"Message": "Successfully logged out"}
    else:
        return {"Message": "Not logged in to log out!"}
