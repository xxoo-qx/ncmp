import logging

class Logger:
    def __init__(self):
        # 配置日志格式
        logging.basicConfig(
            level=logging.DEBUG,  # 改为 DEBUG 级别以显示更多信息
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def end(self, message: str, is_error: bool = False) -> None:
        if is_error:
            self.error(message)
        else:
            self.info(message)