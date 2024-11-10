from fastapi import Depends, HTTPException, status
from typing import Annotated, Optional, List

# from models.passworddb import Password
from cryptography.fernet import Fernet

KEY = "g05kB3VppBksCACXhqd5jxZJNJ6xmJZqQJy4WxgU7X4="


class EncryptionService:

    def __init__(self):
        self.cipher = Fernet(KEY)

    def encrypt_password(self, plain_password: str) -> str:
        return self.cipher.encrypt(plain_password.encode()).decode()

    def decrypt_password(self, encrypted_password: str) -> str:
        return self.cipher.decrypt(encrypted_password.encode()).decode()
