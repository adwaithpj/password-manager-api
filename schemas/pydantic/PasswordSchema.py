from pydantic import BaseModel


class PasswordGetSchema(BaseModel):
    id: int
    user_id: int
    website_name: string
    username_email: string
    password: string
