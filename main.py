from config import Config
from music_partner_bot import MusicPartnerBot
from logger import Logger
from cookie_validator import CookieValidator
import smtplib
from email.mime.text import MIMEText
import os
import requests

class NotificationService:
    def __init__(self, config):
        self.config = config
        # 从环境变量或配置文件获取邮箱配置
        self.email = os.getenv("NOTIFY_EMAIL") or config.get("notify_email", "")
        self.email_password = os.getenv("EMAIL_PASSWORD") or config.get("email_password", "")
        self.smtp_server = os.getenv("SMTP_SERVER") or config.get("smtp_server", "")
        self.smtp_port = os.getenv("SMTP_PORT") or config.get("smtp_port", "")
        
    def send_notification(self, subject: str, message: str) -> None:
        """发送通知"""
        if not self.email or not self.email_password:
            return
        
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = self.email

            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email, self.email_password)
                server.send_message(msg)
        except Exception as e:
            print(f"发送通知失败: {str(e)}")

def main():
    try:
        config = Config()
        logger = Logger()
        notifier = NotificationService(config)
        
        # 创建会话
        session = requests.Session()
        
        # 验证Cookie
        validator = CookieValidator(session, logger)
        is_valid, message = validator.validate()
        
        if not is_valid:
            logger.error(message)
            notifier.send_notification(
                "网易云音乐合伙人 - Cookie失效提醒", 
                f"请更新Cookie\n详细信息: {message}"
            )
            return
        
        # 运行主程序
        bot = MusicPartnerBot(config, logger)
        success = bot.run()
        
        # 发送执行结果通知
        end_message = "✅ 执行成功" if success else "❌ 执行失败"
        logger.end(end_message, not success)
        
        if not success:
            notifier.send_notification(
                "网易云音乐合伙人 - 执行失败提醒",
                f"程序执行失败，请检查日志"
            )
            
    except Exception as e:
        logger = Logger()
        error_message = f"程序异常: {str(e)}"
        logger.error(error_message)
        logger.end("❌ 执行失败", True)
        
        notifier.send_notification(
            "网易云音乐合伙人 - 异常提醒",
            error_message
        )

if __name__ == "__main__":
    main() 