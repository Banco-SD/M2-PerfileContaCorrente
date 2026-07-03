from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.wallet_repository import WalletRepository
from app.utils.exceptions import (
    InsufficientFundsException,
    InvalidWalletOperationException,
    WalletNotFoundException,
)
from app.models.wallet import Wallet
from app.schemas.wallet import WalletTransactionRequest


class WalletService:
    def __init__(self, repository: WalletRepository) -> None:
        self.repository = repository

    def get_wallet(self, db: Session, user_id: UUID) -> Wallet:
        wallet = self.repository.get_wallet_by_user_id(db, user_id)
        if wallet is None:
            raise WalletNotFoundException(detail="Usuário não encontrado")
        return wallet

    def get_or_create_wallet(self, db: Session, user_id: UUID) -> Wallet:
        try:
            return self.repository.get_or_create_wallet(db, user_id)
        except Exception:
            db.rollback()
            raise

    def get_statement(self, db: Session, user_id: UUID):
        wallet = self.get_wallet(db, user_id)
        return self.repository.get_statements_by_wallet_id(db, wallet.id)

    def debit(self, db: Session, payload: WalletTransactionRequest) -> Wallet:
        try:
            wallet = self.repository.get_wallet_by_user_id(db, payload.user_id, for_update=True)
            if wallet is None:
                raise WalletNotFoundException(detail="Usuário não encontrado")

            if wallet.status.upper() != "ATIVA":
                raise InvalidWalletOperationException(detail="Carteira inativa")

            if wallet.saldo - payload.valor < Decimal("0"):
                raise InsufficientFundsException(detail="Saldo insuficiente")

            wallet.saldo -= payload.valor
            wallet.updated_at = datetime.utcnow()
            self.repository.create_statement(
                db=db,
                wallet_id=wallet.id,
                tipo="DEBITO",
                valor=payload.valor,
                descricao=payload.descricao,
                referencia=payload.referencia,
            )
            db.add(wallet)
            db.commit()
            db.refresh(wallet)
            return wallet
        except Exception:
            db.rollback()
            raise

    def credit(self, db: Session, payload: WalletTransactionRequest) -> Wallet:
        try:
            wallet = self.repository.get_wallet_by_user_id(db, payload.user_id, for_update=True)
            if wallet is None:
                raise WalletNotFoundException(detail="Usuário não encontrado")

            if wallet.status.upper() != "ATIVA":
                raise InvalidWalletOperationException(detail="Carteira inativa")

            wallet.saldo += payload.valor
            wallet.updated_at = datetime.utcnow()
            self.repository.create_statement(
                db=db,
                wallet_id=wallet.id,
                tipo="CREDITO",
                valor=payload.valor,
                descricao=payload.descricao,
                referencia=payload.referencia,
            )
            db.add(wallet)
            db.commit()
            db.refresh(wallet)
            return wallet
        except Exception:
            db.rollback()
            raise
