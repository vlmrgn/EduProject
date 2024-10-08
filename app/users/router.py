from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import get_hashed_password, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.users.dao import UsersDAO

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_users = await UsersDAO.find_one_or_none(
        email=user_data.email)  # Проверка наличия пользователя с таким email
    if existing_users:
        raise UserAlreadyExistsException  # Пользователь существует
    hashed_password = get_hashed_password(user_data.password)  # Хеширование пароля
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)  # Добавление пользователя


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)  # Аутентификация пользователя
    if not user:
        raise IncorrectEmailOrPasswordException  # Неправильная почта или пароль
    access_token = create_access_token({'sub': str(user.id)})  # Генерация токена
    response.set_cookie('booking_access_token', access_token, httponly=True)  # Запись токена в куки
    return {'access_token': access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')  # Удаление токена из кук


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user  # Возврат текущего пользователя
