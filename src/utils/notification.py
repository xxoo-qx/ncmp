import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from .config import Config
from .logger import Logger


class NotificationService:
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        
    def send_notification(self, subject: str, content: str) -> bool:
        """发送通知邮件"""
        try:
            notify_email = self.config.get("notify_email")
            if not notify_email:
                self.logger.info("未配置通知邮箱，跳过通知发送")
                return False
                
            email_password = self.config.get("email_password")
            if not email_password:
                self.logger.warning("未配置邮箱密码，无法发送通知")
                return False
                
            smtp_server = self.config.get("smtp_server", "smtp.gmail.com")
            smtp_port = int(self.config.get("smtp_port", 465))
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = notify_email
            msg['To'] = notify_email
            msg['Subject'] = subject
            
            body = MIMEText(content)
            msg.attach(body)
            
            # 尝试使用 SSL 连接发送邮件
            try:
                self.logger.debug(f"尝试使用 SSL 连接到 {smtp_server}:{smtp_port}")
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                    server.login(notify_email, email_password)
                    server.send_message(msg)
            except Exception as ssl_error:
                self.logger.debug(f"SSL 连接失败，尝试使用 TLS: {str(ssl_error)}")
                # 如果 SSL 失败，尝试使用显式 TLS
                with smtplib.SMTP(smtp_server, 587) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(notify_email, email_password)
                    server.send_message(msg)
                
            self.logger.info(f"通知邮件发送成功: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"发送通知邮件失败: {str(e)}")
            return False