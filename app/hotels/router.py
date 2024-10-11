from fastapi import APIRouter

from app.hotels.dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
)


@router.get('id/{hotel_id}')
async def get_hotels_by_id(hotel_id: int):
    return await HotelDAO.find_by_id(hotel_id)
