from typing import List, Optional
from fastapi import Depends, HTTPException, status
from models.passworddb import Password
from starlette import status
from schemas.pydantic.UserSchema import UserGetSchema
from schemas.pydantic.PasswordSchema import (
    PasswordGetSchema,
    PasswordCreateSchema,
    PasswordUpdateSchema,
)
from repositories.PasswordRepository import PasswordRepository
from repositories.Userrepository import UsersRepository
from datetime import datetime, timedelta
from models.passworddb import Password
from services.EncryptionService import EncryptionService

SECRET_KEY = "f11ef682e1b5c7a9c9f617e3432d364621bf4471139f198259743d8f7b7d71a0"
# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    passwordRepository = PasswordRepository

    def __init__(
        self,
        passwordRepository: PasswordRepository = Depends(),
        encryption: EncryptionService = Depends(),
    ) -> None:
        self.passwordRepository = passwordRepository
        self.encryption = encryption

    def list(
        self,
        user_id: int,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Password]:
        return self.passwordRepository.list(user_id, pageSize, startIndex)

    def create(
        self,
        id: int,
        passwordData: PasswordCreateSchema,
    ) -> Password:
        return self.passwordRepository.create(
            Password(
                user_id=id,
                website_name=passwordData.website_name,
                username_email=passwordData.username_email,
                password=self.encryption.encrypt_password(passwordData.password),
            )
        )

    def get(self, id: int, user_id: int):
        password = self.passwordRepository.get(id, user_id)
        if not password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Password not found"
            )

        return password

    def update(
        self, id: int, user_id: int, passwordData: PasswordUpdateSchema
    ) -> Password:
        password = self.passwordRepository.get(id, user_id)
        if not password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Password not found"
            )

        password.username_email = passwordData.username_email
        password.password = self.encryption.encrypt_password(passwordData.password)

        return self.passwordRepository.update(password)

    def delete(self, id: int, user_id: int) -> bool:
        password = self.passwordRepository.get(id, user_id)
        if not password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Password not found"
            )
        return self.passwordRepository.delete(password)
