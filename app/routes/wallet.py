from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.wallet_repository import WalletRepository
from app.schemas.statement import WalletStatementItem
from app.schemas.wallet import WalletResponse, WalletTransactionRequest
from app.services.wallet_service import WalletService
from app.utils.logging import logger

router = APIRouter(prefix="/wallet", tags=["wallet"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}", response_model=WalletResponse)
def get_wallet(user_id: UUID, db: Session = Depends(get_db)) -> WalletResponse:
    logger.info("Consultando saldo para usuário %s", user_id)
    service = WalletService(WalletRepository())
    wallet = service.get_wallet(db, user_id)
    return WalletResponse(user_id=wallet.user_id, saldo=wallet.saldo, status=wallet.status)


@router.get("/{user_id}/statement", response_model=List[WalletStatementItem])
def get_wallet_statement(user_id: UUID, db: Session = Depends(get_db)) -> List[WalletStatementItem]:
    logger.info("Consultando extrato para usuário %s", user_id)
    service = WalletService(WalletRepository())
    statements = service.get_statement(db, user_id)
    return [WalletStatementItem.from_orm(item) for item in statements]


@router.post("/debit", response_model=WalletResponse)
def debit_wallet(payload: WalletTransactionRequest, db: Session = Depends(get_db)) -> WalletResponse:
    logger.info("Débito iniciado para usuário %s valor %s", payload.user_id, payload.valor)
    service = WalletService(WalletRepository())
    wallet = service.debit(db, payload)
    logger.info("Débito concluído para usuário %s", payload.user_id)
    return WalletResponse(user_id=wallet.user_id, saldo=wallet.saldo, status=wallet.status)


@router.post("/credit", response_model=WalletResponse)
def credit_wallet(payload: WalletTransactionRequest, db: Session = Depends(get_db)) -> WalletResponse:
    logger.info("Crédito iniciado para usuário %s valor %s", payload.user_id, payload.valor)
    service = WalletService(WalletRepository())
    wallet = service.credit(db, payload)
    logger.info("Crédito concluído para usuário %s", payload.user_id)
    return WalletResponse(user_id=wallet.user_id, saldo=wallet.saldo, status=wallet.status)
