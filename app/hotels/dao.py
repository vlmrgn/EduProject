from app.dao.base import BaseDao
from app.hotels.models import Hotels


class HotelDAO(BaseDao):
    model = Hotels