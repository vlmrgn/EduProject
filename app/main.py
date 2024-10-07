from fastapi import FastAPI
from app.bookings.router import router as booking_router
from app.users.router import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(booking_router)
