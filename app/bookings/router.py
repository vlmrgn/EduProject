from typing import List

from fastapi import APIRouter
from app.bookings.schemas import SBooking
from app.bookings.dao import BookingDAO

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get('', response_model=List[SBooking])
async def get_bookings():
    return await BookingDAO.find_all()
