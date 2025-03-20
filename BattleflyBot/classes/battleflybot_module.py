from bot_logger import logger

class battleflyBotModule:
    def log_error(self, exc_name: Exception, msg: str, exc: Exception):
        """Logs errors without duplicating timestamps."""
        print(f"{msg} See error.log.")
        logger.error(f"{exc_name}: {msg}\n{str(exc)}")
