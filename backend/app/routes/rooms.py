from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Room, User
from ..schemas import RoomCreate, RoomResponse
from ..auth import get_current_user

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("", response_model=RoomResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_room = Room(name=room.name, owner_id=current_user.id)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("", response_model=List[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return rooms

@router.get("/my", response_model=List[RoomResponse])
def get_my_rooms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rooms = db.query(Room).filter(Room.owner_id == current_user.id).all()
    return rooms

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id, Room.owner_id == current_user.id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found or unauthorized")
    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}