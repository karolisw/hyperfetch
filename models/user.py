import uuid
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from pydantic.networks import email_validator
from pydantic.validators import datetime


# A response body is the data your API sends to the client

# Models the request body of the "Run"-entity (meaning sent by/from client to this API)
# TODO Is it reasonable to ask the user to create a user inside the backend. Could it be part of the pip package?
class User(BaseModel):
    user_id: str = Field(default_factory=uuid.uuid4, alias="user_id")
    email: EmailStr
    password: str


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db
