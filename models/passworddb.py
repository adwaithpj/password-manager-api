from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String, ForeignKey
from sqlalchemy.orm import relationship
from models.BaseModel import EntityMeta


class Password(EntityMeta):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    website_name = Column(String)
    username_email = Column(String)
    password = Column(String)  # This should be a hashed password

    # Back reference to the User
    user = relationship("User", back_populates="passwords")

    def normalize(self):
        return {
            self.id: {
                "id": self.id.__str__(),
                "user_id": self.user_id.__str__(),
                "website_name": self.website_name.__str__(),
                "username_email": self.username_email.__str__(),
                "password": self.website_name.__str__(),
            },
        }
