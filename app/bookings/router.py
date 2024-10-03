from fastapi import APIRouter
from app.bookings.schemas import SBooking
from app.bookings.dao import BookingDAO

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get('', response_model=SBooking)
async def get_bookings():
    return await BookingDAO.find_one_or_none(room_id=1)
