import logging
from datetime import datetime

class Logger:
    def __init__(self):
        # 配置日志格式
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def end(self, message: str, is_error: bool = False) -> None:
        if is_error:
            self.error(message)
        else:
            self.info(message) 