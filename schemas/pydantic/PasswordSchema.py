from pydantic import BaseModel, EmailStr


class PasswordGetSchema(BaseModel):
    id: int
    user_id: int
    website_name: str
    username_email: str
    password: str


class PasswordCreateSchema(BaseModel):
    website_name: str
    username_email: str
    password: str


class PasswordUpdateSchema(BaseModel):
    username_email: str
    password: str
