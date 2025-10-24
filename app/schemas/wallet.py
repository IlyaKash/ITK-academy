from pydantic import BaseModel, ConfigDict, Field, UUID4
from decimal import Decimal
from typing import Literal

class OperationIn(BaseModel):
    """Модель для входящих операций пополнения/снятия"""
    operation_type: Literal["DEPOSIT", "WITHDRAW"]=Field(example="DEPOSIT")
    amount: Decimal=Field(gt=0, max_digits=18, decimal_places=2, example=100.50)

class WalletBase(BaseModel):
    """Базовая модель для кошелька"""
    model_config = ConfigDict(from_attributes=True)

class WalletResponse(WalletBase):
    """Модель ответа с информацией о кошельке"""
    uuid: UUID4
    balance: Decimal
    