from typing import List, Optional

from fastapi import Depends, HTTPException
from models.Userdb import User

# pass word model add here after completing user backend

from repositories.Userrepository import UsersRepository
from services.EncryptionService import EncryptionService
from schemas.pydantic.UserSchema import UserCreateSchema, UserPatchSchema
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    userRepository = UsersRepository

    def __init__(
        self,
        userRepository: UsersRepository = Depends(),
        encryption: EncryptionService = Depends(),
    ) -> None:
        self.userRepository = userRepository
        self.encryption = encryption

    def create(
        self,
        user_body: UserCreateSchema,
    ) -> User:
        pass_main = self.encryption.generate_key()
        # print(pass_main)
        user_check = self.userRepository.get_by_email(email=user_body.email)
        if user_check:
            raise HTTPException(
                status_code=409, detail="User with this email address already exists"
            )
        else:
            return self.userRepository.create(
                User(
                    name=user_body.name,
                    email=user_body.email,
                    hashed_password=bcrypt_context.hash(user_body.hashed_password),
                    pass_key=pass_main,
                )
            )

    def get(
        self, user_id: int, userRepository: UsersRepository = Depends()
    ) -> Optional[User]:
        user = self.userRepository.get(User(id=user_id))
        if not user:
            return False
        return user

    def delete(
        self,
        author_id: int,
    ) -> bool:

        return self.userRepository.delete(author_id)

    def update(self, user_id: int, user_body: UserPatchSchema) -> User:
        print("update serg")
        existing_user = self.get(user_id)
        if not existing_user:
            return False
        if user_body.name:
            existing_user.name = user_body.name

        return self.userRepository.update(user_id, existing_user)
