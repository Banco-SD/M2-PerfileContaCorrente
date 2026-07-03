from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, constr, condecimal


class WalletResponse(BaseModel):
    user_id: UUID
    saldo: Decimal
    status: str

    class Config:
        from_attributes = True
        json_encoders = {Decimal: lambda v: float(v)}


class WalletTransactionRequest(BaseModel):
    user_id: UUID
    valor: condecimal(gt=0, max_digits=15, decimal_places=2)
    descricao: constr(min_length=1, max_length=500)
    referencia: UUID

    class Config:
        str_strip_whitespace = True
