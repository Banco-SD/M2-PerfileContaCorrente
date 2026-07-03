from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.wallet import Wallet
from app.models.wallet_statement import WalletStatement


class WalletRepository:
    def get_wallet_by_user_id(self, db: Session, user_id: UUID, for_update: bool = False) -> Optional[Wallet]:
        statement = select(Wallet).where(Wallet.user_id == user_id)
        if for_update:
            statement = statement.with_for_update()
        result = db.execute(statement)
        return result.scalars().first()

    def get_statements_by_wallet_id(self, db: Session, wallet_id: UUID) -> List[WalletStatement]:
        statement = (
            select(WalletStatement)
            .where(WalletStatement.wallet_id == wallet_id)
            .order_by(WalletStatement.created_at.desc())
        )
        result = db.execute(statement)
        return result.scalars().all()

    def create_statement(
        self,
        db: Session,
        wallet_id: UUID,
        tipo: str,
        valor,
        descricao: str,
        referencia: UUID,
    ) -> WalletStatement:
        statement = WalletStatement(
            wallet_id=wallet_id,
            tipo=tipo,
            valor=valor,
            descricao=descricao,
            referencia=referencia,
        )
        db.add(statement)
        return statement
