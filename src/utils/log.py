from loguru import logger
logger.add("logs/runtime.log", rotation="7 days", enqueue=True, backtrace=True, diagnose=False)
get_logger = lambda: logger
