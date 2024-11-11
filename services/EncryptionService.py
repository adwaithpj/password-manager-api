from fastapi import Depends, HTTPException, status
from typing import Annotated, Optional, List
from starlette import status

# from models.passworddb import Password
from cryptography.fernet import Fernet, InvalidToken

# KEY = "g05kB3VppBksCACXhqd5jxZJNJ6xmJZqQJy4WxgU7X4="


class EncryptionService:

    def key_check(self, key: str):
        """Check if the provided key is valid."""
        try:
            Fernet(key)  # This checks the validity of the key without storing it.
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Key is corrupted",
            )

    def generate_key(self):
        key = Fernet.generate_key()
        # print(key)
        return key.decode()

    def encrypt_password(self, plain_password: str, key: str) -> str:
        self.key_check(key)  # Ensures the key is valid before encrypting
        cipher = Fernet(key.encode())
        return cipher.encrypt(plain_password.encode()).decode()

    def decrypt_password(self, encrypted_password: str, key: str) -> str:
        """Decrypt the password using the provided key."""
        self.key_check(key)  # Ensures the key is valid before decrypting
        cipher = Fernet(key.encode())
        try:
            return cipher.decrypt(encrypted_password.encode()).decode()
        except InvalidToken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid encryption token provided",
            )
