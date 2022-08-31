from uuid import UUID
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    first_name: str = Field(..., description="first name")
    last_name: str = Field(..., description="last name")
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserOut(BaseModel):
    id: int
    email: str


class SystemUser(UserOut):
    hashed_password: str
