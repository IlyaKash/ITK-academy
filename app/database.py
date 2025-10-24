from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import settings

#Формирую строку подключения к бд с использование асинхронного драйвера(asyncpg)
DATABASE_URL=f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

#Все модели будут наследоваться от этой
class Base(DeclarativeBase):
    pass

#Созадю движок
engine=create_async_engine(
    DATABASE_URL,
    echo=True, #Отключю в продакшине

    #Задаю пулы соединений
    pool_size=20, #Постоянные соединения
    max_overflow=30, #Временные при пиковой нагрузке
    pool_pre_ping=True, #Проверять живое ли сиоединение
    pool_recycle=3600 #Обновлять какждый час
)

#И создаю фабрику сессий
async_session_maker=async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#Создаю зависимость для FastAPI чтоб использовать Depends
async def get_async_session()->AsyncGenerator[AsyncSession, None]:
    """
        Генератор асинхронных сессий.
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
