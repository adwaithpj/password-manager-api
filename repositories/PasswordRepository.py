from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session, lazyload
from configs.Database import (
    get_db_connection,
)
from models.passworddb import Password
from schemas.pydantic.PasswordSchema import (
    PasswordGetSchema,
    PasswordCreateSchema,
    PasswordUpdateSchema,
)


class PasswordRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(
        self,
        user_id: int,
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Password]:
        query = self.db.query(Password).filter(Password.user_id == user_id)

        return query.offset(start).limit(limit).all()

    def create(self, password: Password):
        self.db.add(password)
        self.db.commit()
        self.db.refresh(password)
        return password

    def get(self, password_id: int, user_id: int) -> Optional[Password]:
        return (
            self.db.query(Password)
            .filter(Password.id == password_id, Password.user_id == user_id)
            .first()
        )

    def update(self, password_data: Password) -> Optional[Password]:
        existing_password = (
            self.db.query(Password).filter(Password.id == password_data.id).first()
        )
        if not existing_password:
            return None  # Optionally, handle cases where password doesn't exist

        # Update the fields of the retrieved password instance
        existing_password.username_email = password_data.username_email
        existing_password.password = (
            password_data.password
        )  # Assuming it's already encrypted

        # Commit the changes and refresh the instance
        self.db.commit()
        self.db.refresh(existing_password)
        return existing_password

    def delete(self, password: Password) -> True:
        self.db.delete(password)
        self.db.commit()
        self.db.flush()
        return True
