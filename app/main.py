from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.bookings.router import router as booking_router
from app.users.router import router as user_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as rooms_router

app = FastAPI()
app.include_router(user_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(rooms_router)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis=redis), prefix="cache")