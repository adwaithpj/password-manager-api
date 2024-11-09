from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session, lazyload
from configs.Database import (
    get_db_connection,
)
from models.Userdb import User


class UsersRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get(self, user: User) -> User:
        return self.db.get(User, user.id)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, id: int) -> bool:
        try:
            self.db.query(User).filter(User.id == id).delete()
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def update(self, id: int, user: User) -> User:
        print("update repo")
        user.id = id
        self.db.merge(user)
        self.db.commit()
        return user
