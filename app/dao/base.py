from sqlalchemy import select, insert
from app.database import async_session_maker


class BaseDao:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:  # Подключение к базе данных
            query = select(cls.model).filter_by(id=model_id)  # Cоздание запроса
            result = await session.execute(query)  # Выполнение запроса
            return result.scalar_one_or_none()  # Возвращение результата

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()  # Сохранение изменений
