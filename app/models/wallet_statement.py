import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class WalletStatement(Base):
    __tablename__ = "wallet_statement"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallet.id"), nullable=False)
    tipo = Column(String(20), nullable=False)
    valor = Column(Numeric(15, 2), nullable=False)
    descricao = Column(Text, nullable=False)
    referencia = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    wallet = relationship("Wallet", back_populates="statements")
