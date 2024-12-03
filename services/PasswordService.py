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
from configs.Environment import get_environment_variables

env = get_environment_variables()

SECRET_KEY = f"{env.SECRET_KEY}"
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
        pass_key: str,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Password]:
        password_list = self.passwordRepository.list(user_id, pageSize, startIndex)
        for pwd in password_list:
            pwd.password = self.encryption.decrypt_password(pwd.password, key=pass_key)
        return password_list

    def create(
        self,
        id: int,
        passwordData: PasswordCreateSchema,
        pass_key: str,
    ) -> Password:
        # print(pass_key)
        return self.passwordRepository.create(
            Password(
                user_id=id,
                website_name=passwordData.website_name,
                username_email=passwordData.username_email,
                password=self.encryption.encrypt_password(
                    passwordData.password,
                    key=pass_key,
                ),
            )
        )

    def get(self, id: int, user_id: int, pass_key: str):
        password = self.passwordRepository.get(id, user_id)
        if not password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Password not found"
            )
        password.password = self.encryption.decrypt_password(
            password.password, key=pass_key
        )
        return password

    def update(
        self, id: int, user_id: int, pass_key: str, passwordData: PasswordUpdateSchema
    ) -> Password:
        password = self.passwordRepository.get(id, user_id)
        if not password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Password not found"
            )

        password.username_email = passwordData.username_email
        password.password = self.encryption.encrypt_password(
            passwordData.password, key=pass_key
        )

        return self.passwordRepository.update(password)

    def delete(self, id: int, user_id: int) -> bool:
        password = self.passwordRepository.get(id, user_id)
        if not password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Password not found"
            )
        return self.passwordRepository.delete(password)
