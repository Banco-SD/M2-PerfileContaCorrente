import logging


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger = logging.getLogger("wallet_service")
    logger.setLevel(logging.INFO)


logger = logging.getLogger("wallet_service")
