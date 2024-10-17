import asyncio
from datetime import date
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.bookings.dao import BookingDAO
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get('')
@cache(100)
async def get_bookings(user: Users = Depends(get_current_user)):
    await asyncio.sleep(4)
    return await BookingDAO.find_all(user_id=user.id)


@router.post('')
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked


@router.delete('/{booking_id}')
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    return await BookingDAO.delete(booking_id, user.id)
