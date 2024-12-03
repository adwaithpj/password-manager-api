from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    user_name: str


class TokenDataSchema(BaseModel):
    username: str | None = None
