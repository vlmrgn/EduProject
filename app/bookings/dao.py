from datetime import date

from sqlalchemy import and_, or_, func, select
from sqlalchemy.dialects.mysql import insert

from app.bookings.models import Booking
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.rooms.models import Rooms


class BookingDAO(BaseDao):
    model = Booking

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date
                  ):
        async with async_session_maker() as session:
            booked_rooms = select(Booking).where(
                and_(
                    Booking.room_id == room_id,
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_from <= date_to
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to > date_from
                        ),
                    )
                )
            ).cte('booked_rooms')

            get_rooms_left = select(
                Rooms.quantity - func.count(booked_rooms.c.room_id)
            ).select_from(Rooms).join(
                booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()  # кол-во свободных комнат

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)  # цена комнаты
                price = await session.execute(get_price)
                price = price.scalar()  # цена комнаты

                # добавление брони
                add_booking = insert(Booking).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Booking)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
