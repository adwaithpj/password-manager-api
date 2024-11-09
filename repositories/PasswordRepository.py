from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session, lazyload
from configs.Database import (
    get_db_connection,
)
from models.passworddb import Password
from schemas.pydantic.PasswordDBSchema import PasswordGetSchema


class PasswordRepository:
    db: Sesssion

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(self) -> List[Book]:
        pass

    def create(self):
        pass

    def get(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
