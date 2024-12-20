from config import Config
from music_partner_bot import MusicPartnerBot
from logger import Logger
from cookie_validator import CookieValidator
import smtplib
from email.mime.text import MIMEText
import os
import requests


class NotificationService:
    def __init__(self, config, logger):  # 修改构造函数
        self.config = config
        self.logger = logger
        self.email = os.getenv("NOTIFY_EMAIL") or config.get("notify_email")
        self.email_password = os.getenv("EMAIL_PASSWORD") or config.get("email_password")
        self.smtp_server = os.getenv("SMTP_SERVER") or "smtp.gmail.com"
        self.smtp_port = int(os.getenv("SMTP_PORT") or 465)
        
    def send_notification(self, subject: str, message: str) -> None:
        """发送邮件通知"""
        if not self.email or not self.email_password:
            self.logger.warning("邮件配置不完整，跳过发送通知")
            return
        
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = self.email
            self.logger.debug(f"当前代理设置: HTTP_PROXY={os.environ.get('http_proxy')}, HTTPS_PROXY={os.environ.get('https_proxy')}")
            self.logger.debug(f"尝试连接: {self.smtp_server}:{self.smtp_port}")
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email, self.email_password)
                server.send_message(msg)
        except Exception as e:
            print(f"发送通知失败: {str(e)}")

def main():
    try:
        config = Config()
        logger = Logger()
        notifier = NotificationService(config, logger)  # 确保在这里就创建好
        
        # 创建会话并设置Cookie
        session = requests.Session()
        required_cookies = {
            "MUSIC_U": config.get("Cookie_MUSIC_U"),
            "__csrf": config.get("Cookie___csrf")
        }
        for name, value in required_cookies.items():
            session.cookies.set(name, value)
        
        # 验证Cookie
        try:
            validator = CookieValidator(session, logger)
            is_valid, message = validator.validate()
            
            if not is_valid:
                logger.error(message)
                # 使用try-except专门处理通知发送
                try:
                    notifier.send_notification(
                        "网易云音乐合伙人 - Cookie失效提醒", 
                        f"请更新Cookie\n详细信息: {message}"
                    )
                except Exception as e:
                    logger.error(f"发送Cookie失效通知时出错: {str(e)}")
                return
                
        except Exception as e:
            logger.error(f"Cookie验证过程出错: {str(e)}")
            try:
                notifier.send_notification(
                    "网易云音乐合伙人 - 验证异常",
                    f"Cookie验证过程出错\n详细信息: {str(e)}"
                )
            except Exception as notify_error:
                logger.error(f"发送验证异常通知时出错: {str(notify_error)}")
            return
        
        # 使用同一个session运行主程序
        bot = MusicPartnerBot(config, logger, session)
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
        error_message = f"程序异常: {str(e)}"
        logger.error(error_message)
        logger.end("❌ 执行失败", True)
        
        try:
            notifier.send_notification(
                "网易云音乐合伙人 - 异常提醒",
                error_message
            )
        except Exception as notify_error:
            logger.error(f"发送异常通知时出错: {str(notify_error)}")

if __name__ == "__main__":
    main()