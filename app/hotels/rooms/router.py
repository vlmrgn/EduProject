from app.hotels.rooms.dao import RoomDAO
from fastapi import APIRouter

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
)


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_hotel_id(hotel_id: int):
    return await RoomDAO.find_all(hotel_id=hotel_id)
