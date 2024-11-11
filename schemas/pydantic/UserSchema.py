from pydantic import BaseModel, EmailStr, Field, validator


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    hashed_password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description="Password must be between 8 and 50 characters",
    )

    @validator("hashed_password")
    def validate_password(cls, value):
        if "#" in value:
            raise ValueError("Password should not contain '@' or '#' characters")
        return value


class UserGetSchema(UserBaseSchema):
    id: int


class UserCredSchema(UserBaseSchema):
    id: int
    pass_key: str


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserPatchSchema(BaseModel):
    name: str
