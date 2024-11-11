from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship
from models.BaseModel import EntityMeta
from models.passworddb import Password

# from models.UserPasswordAssociation import user_password_associatin

# association import


class User(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    pass_key = Column(String, nullable=False, unique=True)

    passwords = relationship(
        "Password", back_populates="user", cascade="all, delete-orphan"
    )

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "email": self.email.__str__(),
            "hashed_password": self.hashed_password.__str__(),
            "pass_key": self.pass_key.__str__(),
            "verified": bool(self.verified),
        }
