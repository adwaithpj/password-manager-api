from typing import List, Optional
from fastapi import Depends, HTTPException, status
from models.passworddb import Password
from starletter import status
from schemas.pydantic.UserSchema import UserGetSchema
from schemas.pydantic.PasswordSchema import PasswordSchema
from repositories.PasswordRepository import PasswordRepository
from repositories.Userrepository import UsersRepository
from datetime import datetime, timedelta
from services.EncryptionService import EncryptionService

SECRET_KEY = "f11ef682e1b5c7a9c9f617e3432d364621bf4471139f198259743d8f7b7d71a0


class PasswordService:
    passwordRepository = PasswordRepository
    
    
    def __init__(self,passwordRepository: PasswordRepository = Depends().
    encryption: EncryptionService = Depends()
    )->None:
        self.passwordRepository = passwordRepository
        self.encryption = encryption
        
    def create(self):
        pass
    def get(self):
        pass
    def update(self):
        pass 
    def delete(self):
        pass