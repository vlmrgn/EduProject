from datetime import datetime, timezone

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UserIsNotPresentException
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")  # Получение токена из кук
    if not token:
        raise TokenAbsentException  # Токен отсутствует
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)  # Декодирование токена
    except JWTError:
        raise IncorrectTokenFormatException  # Неправильный формат токена
    expire: str = payload.get("exp")  # Срок действия
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):  # Проверка срока действия
        raise TokenExpiredException  # Токен истек
    user_id = int(payload.get("sub"))  # Идентификатор пользователя
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(user_id)  # Поиск пользователя
    if not user:
        raise UserIsNotPresentException
    return user  # Возврат пользователя
