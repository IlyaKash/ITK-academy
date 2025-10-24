from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.wallet import Wallet
from app.schemas.wallet import WalletResponse, OperationIn
from sqlalchemy.exc import SQLAlchemyError

class WalletCRUD():
    def __init__(self, session: AsyncSession):
        self.session=session

    async def get(self, wallet_uuid: str) -> WalletResponse | None:
        """
            Получить кошелек по UUID
        """
        try:
            result=await self.session.execute(
                select(Wallet).where(Wallet.uuid==wallet_uuid)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
                raise
    
    #Пускай если такого UUID не будет будет создан Wallet в бд 
    async def create(self) -> WalletResponse:
        """
            Создать новый кошелек
        """
        try:
            wallet=Wallet()
            self.session.add(wallet)
            await self.session.commit()
            await self.session.refresh(wallet)
            return wallet
        except SQLAlchemyError as e:
                await self.session.rollback()
                raise


    async def update(self, wallet_uuid: str, operation: OperationIn) -> WalletResponse:
        """
            Выполнение обновления счета в бд
        """
        max_retries=3
        for attempt in range(max_retries):
            try:
                #Начало транзакции
                result=await self.session.execute(
                    select(Wallet).where(Wallet.uuid==wallet_uuid).with_for_update()
                )
                wallet=result.scalar_one_or_none()
                if not wallet:
                    raise ValueError("Wallet not found")
                    
                #Вополняю операцию
                if operation.operation_type=="DEPOSIT":
                    wallet.balance+=operation.amount
                elif operation.operation_type=="WITHDRAW":
                    if wallet.balance < operation.amount:
                        raise ValueError("Insufficient funds")
                    wallet.balance -= operation.amount
                await self.session.commit()
                await self.session.refresh(wallet)
                print(f"Wallet {wallet_uuid} new balance: {wallet.balance}")
                return wallet
            except SQLAlchemyError as e:
                await self.session.rollback()
                if "could not serialize access" in str(e) and attempt < max_retries - 1:
                    continue
                else:
                    raise
            except ValueError as e:
                await self.session.rollback()
                raise
        raise Exception("Max retries exceeded")
    
