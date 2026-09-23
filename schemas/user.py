from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)

    username: str = Field(..., min_length=3, max_length=50)

    email: EmailStr

    phone: str = Field(..., min_length=10, max_length=20)

    password: str = Field(..., min_length=6, max_length=100)

    blood_group: str | None = None
    location: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None

    phone: str | None = None

    blood_group: str | None = None
    location: str | None = None

    is_available: bool | None = None


class UserResponse(BaseModel):
    id: int

    first_name: str
    last_name: str

    username: str
    email: EmailStr

    phone: str

    blood_group: str | None
    location: str | None

    role: str

    is_active: bool
    is_available: bool

    created_at: datetime

    class Config:
        from_attributes = True