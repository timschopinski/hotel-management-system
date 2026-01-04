from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from typing import List, Optional
from datetime import date
from ..database import get_db
from ..models import Reservation, Room, User
from ..schemas import ReservationCreate, ReservationUpdate, ReservationResponse
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
def get_my_reservations(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        room_id: Optional[int] = Query(None),
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None),
        guest_name: Optional[str] = Query(None),
        sort_by: Optional[str] = Query("created_at"),
        sort_order: Optional[str] = Query("desc")
):
    query = db.query(Reservation).join(Room).filter(Room.owner_id == current_user.id)

    if room_id:
        query = query.filter(Reservation.room_id == room_id)
    if start_date:
        query = query.filter(Reservation.start_date >= start_date)
    if end_date:
        query = query.filter(Reservation.end_date <= end_date)
    if guest_name:
        query = query.filter(Reservation.guest_name.ilike(f"%{guest_name}%"))

    if sort_order == "asc":
        query = query.order_by(asc(getattr(Reservation, sort_by)))
    else:
        query = query.order_by(desc(getattr(Reservation, sort_by)))

    reservations = query.all()
    return reservations


@router.patch("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
        reservation_id: int,
        reservation_update: ReservationUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    reservation = db.query(Reservation).join(Room).filter(
        Reservation.id == reservation_id,
        Room.owner_id == current_user.id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found or unauthorized")

    if reservation_update.notes is not None:
        reservation.notes = reservation_update.notes

    db.commit()
    db.refresh(reservation)
    return reservation