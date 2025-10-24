import uuid
from sqlalchemy import CheckConstraint, Column, Integer, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Wallet(Base):
    """
        Модель данных Wallet
        Содержит:
        id - первичный ключ
        uuid - уникальный идентификатор
        balacne - баланс кошелька

        Wallet Data Model
        Contains:
        id - primary key
        uuid - unique identifier
        balacne - wallet balance
    """
    __tablename__="wallets"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Автоинкрементный ID"
    )
    uuid = Column(
        String(36), 
        unique=True, 
        index=True, 
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        comment="Уникальный идентификатор кошелька"
    )
    balance = Column(
        Numeric(18, 2), 
        nullable=False, 
        default=0.00,
        comment="Текущий баланс кошелька"
    )

    #Предполагаю что баланс не может быть отрицательный поэтому добаляю ограничение на баланс
    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_positive'),
    )