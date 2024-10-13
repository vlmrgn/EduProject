from fastapi import APIRouter

from app.hotels.dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
)


@router.get('/{location}')
async def get_hotels(location: str):
    return await HotelDAO.find_all(location=location)

@router.get('/id/{hotel_id}')
async def get_hotels_by_id(hotel_id: int):
    return await HotelDAO.find_by_id(hotel_id)
