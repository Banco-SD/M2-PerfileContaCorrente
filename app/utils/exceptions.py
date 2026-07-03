from fastapi import HTTPException


class WalletServiceException(HTTPException):
    pass


class WalletNotFoundException(WalletServiceException):
    def __init__(self, detail: str = "Carteira não encontrada"):
        super().__init__(status_code=404, detail=detail)


class InsufficientFundsException(WalletServiceException):
    def __init__(self, detail: str = "Saldo insuficiente"):
        super().__init__(status_code=409, detail=detail)


class InvalidWalletOperationException(WalletServiceException):
    def __init__(self, detail: str = "Operação inválida na carteira"):
        super().__init__(status_code=400, detail=detail)
