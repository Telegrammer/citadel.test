import logging


log = logging.getLogger(__name__)


def log_info(err: Exception) -> None:
    log.info("Обработано исключение: %s - %s", type(err).__name__, err)


def log_error(err: Exception) -> None:
    log.error("Обработано исключение: %s - %s", type(err).__name__, err)
