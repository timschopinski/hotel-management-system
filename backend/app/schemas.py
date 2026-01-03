from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    name: str

class RoomResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ReservationCreate(BaseModel):
    room_id: int
    guest_name: str
    guest_email: EmailStr
    start_date: date
    end_date: date

class ReservationResponse(BaseModel):
    id: int
    room_id: int
    guest_name: str
    guest_email: str
    start_date: date
    end_date: date
    created_at: datetime
    room: Optional[RoomResponse] = None

    class Config:
        from_attributes = True