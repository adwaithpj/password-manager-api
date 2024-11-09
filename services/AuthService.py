from typing import List, Optional, Annotated

from fastapi import Depends, HTTPException, status
from models.Userdb import User
from starlette import status
from schemas.pydantic.authSchema import TokenSchema, TokenDataSchema
from schemas.pydantic.UserSchema import UserLoginSchema, UserGetSchema
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from repositories.Userrepository import UsersRepository
from datetime import datetime, timedelta

SECRET_KEY = "f11ef682e1b5c7a9c9f617e3432d364621bf4471139f198259743d8f7b7d71a0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


class AuthService:
    userRepository = UsersRepository

    def __init__(self, userRepository: UsersRepository = Depends()) -> None:
        self.userRepository = userRepository

    # def login(self, user: UserLoginSchema) -> Optional[TokenSchema]:
    #     user_login = self.authenticate_user(user)
    #     if user_login == -1:
    #         raise HTTPException(status_code=404, detail="Could not Find User")
    #     elif user_login == 0:
    #         raise HTTPException(status_code=401, detail="Password is incorrect")
    #     token = self.create_access_token(
    #         user_login.email, user_login.id, timedelta(minutes=10)
    #     )

    #     return {"access_token": token, "token_type": "bearer"}

    def login(self, email: str, password: str) -> TokenSchema:
        # Validate user credentials
        user_login = self.authenticate_user(email, password)
        if user_login == -1:
            raise HTTPException(status_code=404, detail="User not found")
        elif user_login == 0:
            raise HTTPException(status_code=401, detail="Incorrect password")

        # Create JWT token
        token = self.create_access_token(
            email=user_login.email,
            user_id=user_login.id,
            expires_delta=timedelta(minutes=10),
        )
        return {"access_token": token, "token_type": "bearer"}

    def create_access_token(self, email: str, user_id: int, expires_delta: timedelta):
        encode = {"sub": email, "id": user_id}
        expires = datetime.utcnow() + expires_delta
        encode.update({"exp": expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    def authenticate_user(self, email: str, password: str):
        fetched_user = self.userRepository.get_by_email(email)
        if not fetched_user:
            return -1
        if not bcrypt_context.verify(password, fetched_user.hashed_password):
            return 0
        return fetched_user

    async def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_bearer)],
        userRepository: UsersRepository = Depends(),
    ) -> Optional[UserGetSchema]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("id")
            if email is None or user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = userRepository.get_by_email(email)
        if user is None:
            raise credentials_exception

        return UserGetSchema(id=user.id, name=user.name, email=user.email)