from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str


class UserRegistered(BaseModel):
    id: UUID


class UserLogin(BaseModel):
    email: str
    password: str


class UserEntered(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserRead(BaseModel):
    email: str
    created_at: datetime
    is_admin: bool


class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str


class UserActivationKeyUpdated(BaseModel):
    email: str


class UserAuth(BaseModel):
    id: UUID
