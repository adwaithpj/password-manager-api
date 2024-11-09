from fastapi import Depends, HTTPException, status
from typing import Annotated, Optional, List

# from models.passworddb import Password
from cryptography.fernet import Fernet

KEY = "f11ef682e1b5c7a9c9f617e3432d364621bf4471139f198259743d8f7b7d71a0"
cipher = Fernet(KEY)


class EncryptionService:

    def encrypt_password(plain_password: str) -> str:
        return cipher.encrypt(plain_password.encode()).decode()

    def decrypt_password(encrypted_password: str) -> str:
        return cipher.decrypt(encrypted_password.encode()).decode()
