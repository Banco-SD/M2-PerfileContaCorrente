import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.routes.health import router as health_router
from app.routes.wallet import router as wallet_router
from app.utils.exceptions import WalletServiceException
from app.utils.logging import configure_logging, logger

configure_logging()

app = FastAPI(title=settings.APP_NAME, version="1.0.0")
app.include_router(health_router)
app.include_router(wallet_router)


@app.middleware("http")
async def log_http_requests(request: Request, call_next):
    start_time = time.time()
    logger.info("Iniciando requisição %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(
            "Requisição finalizada %s %s status=%s tempo=%.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
        return response
    except Exception as error:
        logger.exception("Erro não tratado durante a requisição")
        raise error


@app.exception_handler(WalletServiceException)
async def wallet_service_exception_handler(request: Request, exc: WalletServiceException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    logger.exception("Erro interno do servidor")
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})
