from typing import Optional, List

import uvicorn
from fastapi import FastAPI, Query
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as booking_router

app = FastAPI()
app.include_router(booking_router)

class SHotels(BaseModel):
    address: str
    name: str
    stars: int
    has_spa: bool

@app.get("/hotels/", response_model=List[SHotels])
def get_hotels(
        location: str,
        data_from: date,
        data_to: date,
        stars: Optional[int] = Query(None, ge=1, le=5),
        has_spa: Optional[bool] = None,
):

    hotels = [
        {'address': 'Moscow', 'name': 'Lux', 'stars': 5 },
    ]
    return hotels


class SBooking(BaseModel):
    room_id: int
    data_from: date
    data_to: date


@app.post("/bookings")
def add_bookings(booking: SBooking):
    pass