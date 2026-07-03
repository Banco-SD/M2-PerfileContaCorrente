from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel


class WalletStatementItem(BaseModel):
    id: UUID
    wallet_id: UUID
    tipo: str
    valor: Decimal
    descricao: str
    referencia: UUID
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {Decimal: lambda v: float(v)}


class WalletStatementResponse(BaseModel):
    statements: List[WalletStatementItem]
