from datetime import datetime, timezone

from fastapi import HTTPException, Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")  # Получение токена из кук
    if not token:
        raise HTTPException(status_code=401)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)  # Декодирование токена
    except JWTError:
        raise HTTPException(status_code=401)
    expire: str = payload.get("exp")  # Срок действия
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):  # Проверка срока действия
        raise HTTPException(status_code=401)
    user_id = int(payload.get("sub"))  # Идентификатор пользователя
    user = await UsersDAO.find_by_id(user_id)  # Поиск пользователя
    if not user:
        raise HTTPException(status_code=401)
    return user  # Возврат пользователя
