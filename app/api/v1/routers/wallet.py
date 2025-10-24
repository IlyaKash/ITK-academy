from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.schemas.wallet import OperationIn, WalletResponse
from app.crud.wallet import WalletCRUD

router=APIRouter()

@router.post(
    "/wallets/{wallet_uuid}/operation",
    response_model=WalletResponse,
    status_code=status.HTTP_200_OK
)
async def excute_operation(
    wallet_uuid: str,
    operation: OperationIn,
    session:AsyncSession=Depends(get_async_session)
):
    """Выполнить операцию с кошельком"""
    try:
        crud=WalletCRUD(session)
        wallet=await crud.update(wallet_uuid, operation)
        return wallet
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        elif "funds" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient funds"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get(
    "/wallets/{wallet_uuid}",
    response_model=WalletResponse,
    status_code=status.HTTP_200_OK
)
async def get_wallet(
    wallet_uuid: str,
    session: AsyncSession=Depends(get_async_session)
):
    """Получить информацию о кошельке"""
    crud=WalletCRUD(session)
    wallet=await crud.get(wallet_uuid)

    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    
    return wallet

@router.post(
    "/wallets",
    response_model=WalletResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_wallet(
    session: AsyncSession=Depends(get_async_session)
):
    """
        Создать новый кошелек
    """
    crud=WalletCRUD(session)
    wallet=await crud.create()
    return wallet