import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(name)s '
        'request_id=%(request_id)s message="%(message)s"'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
