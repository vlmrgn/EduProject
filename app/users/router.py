from fastapi import APIRouter, HTTPException, Response

from app.users.auth import get_hashed_password, authenticate_user, create_access_token
from app.users.schemas import SUserAuth
from app.users.dao import UsersDAO

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_users = await UsersDAO.find_one_or_none(email=user_data.email) # Проверка наличия пользователя с таким email
    if existing_users:
        raise HTTPException(status_code=400)
    hashed_password = get_hashed_password(user_data.password) # Хеширование пароля
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password) # Добавление пользователя


@router.post("/login")
async def login_user(response: Response,user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password) # Аутентификация пользователя
    if not user:
        raise HTTPException(status_code=401)
    access_token = create_access_token({'sub': str(user.id)}) # Генерация токена
    response.set_cookie('booking_access_token', access_token, httponly=True) # Запись токена в куки
    return {'access_token': access_token}