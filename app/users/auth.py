from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)  # Хеширование пароля


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)  # Проверка пароля


def create_access_token(data: dict) -> str:
    to_encode = data.copy()  # Копирование словаря
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # Срок действия токена
    to_encode.update({"exp": expire})  # Обновление словаря
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)  # Генерация токена
    return encoded_jwt  # Возврат токена


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)  # Проверка наличия пользователя с таким email
    if not user and not verify_password(password, user.hashed_password):  # Проверка пароля
        return None
    return user  # Возврат пользователя
