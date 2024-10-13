from app.dao.base import BaseDao
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from sqlalchemy import select


class RoomDAO(BaseDao):
    model = Rooms

    @classmethod
    async def find_by_id(cls, hotel_id: int):
        async with async_session_maker() as session:
            query = select(Rooms).filter_by(hotel_id=hotel_id)
            result = await session.execute(query)
            return result.mappings().all()