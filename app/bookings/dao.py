from app.bookings.models import Booking
from app.dao.base import BaseDao


class BookingDAO(BaseDao):
    model = Booking