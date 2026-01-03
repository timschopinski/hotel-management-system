from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from ..database import get_db
from ..models import Reservation, Room, User
from ..schemas import ReservationCreate, ReservationResponse
from ..auth import get_current_user

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == reservation.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if reservation.start_date >= reservation.end_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    conflicting = db.query(Reservation).filter(
        and_(
            Reservation.room_id == reservation.room_id,
            or_(
                and_(
                    Reservation.start_date <= reservation.start_date,
                    Reservation.end_date > reservation.start_date
                ),
                and_(
                    Reservation.start_date < reservation.end_date,
                    Reservation.end_date >= reservation.end_date
                ),
                and_(
                    Reservation.start_date >= reservation.start_date,
                    Reservation.end_date <= reservation.end_date
                )
            )
        )
    ).first()

    if conflicting:
        raise HTTPException(status_code=400, detail="Room is not available for selected dates")

    new_reservation = Reservation(**reservation.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


@router.get("/room/{room_id}", response_model=List[ReservationResponse])
def get_room_reservations(room_id: int, db: Session = Depends(get_db)):
    reservations = db.query(Reservation).filter(Reservation.room_id == room_id).all()
    return reservations


@router.get("/my", response_model=List[ReservationResponse])
def get_my_reservations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reservations = db.query(Reservation).join(Room).filter(Room.owner_id == current_user.id).all()
    return reservations