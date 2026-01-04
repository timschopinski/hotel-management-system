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
    description: Optional[str] = None
    image_url: Optional[str] = None

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class RoomResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
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
    notes: Optional[str] = None

class ReservationUpdate(BaseModel):
    notes: Optional[str] = None

class ReservationResponse(BaseModel):
    id: int
    room_id: int
    guest_name: str
    guest_email: str
    start_date: date
    end_date: date
    notes: Optional[str] = None
    created_at: datetime
    room: Optional[RoomResponse] = None

    class Config:
        from_attributes = True