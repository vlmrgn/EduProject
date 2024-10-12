from app.hotels.router import router


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_hotel_id():
    pass