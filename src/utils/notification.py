import smtplib
from email.mime.text import MIMEText
from typing import Optional
from .logger import Logger

class NotificationService:
    def __init__(self, config, logger: Logger):
        self.config = config
        self.logger = logger
        self.email = config.get("notify_email")
        self.email_password = config.get("email_password")
        self.smtp_server = config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = int(config.get("smtp_port", 465))
        
    def send_notification(self, subject: str, message: str) -> None:
        """发送邮件通知"""
        if not self._check_email_config():
            self.logger.warning("邮件配置不完整，跳过发送通知")
            return
        
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = self.email

            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email, self.email_password)
                server.send_message(msg)
                
            self.logger.info(f"通知邮件发送成功: {subject}")
            
        except Exception as e:
            error_msg = str(e)
            if "qq" in self.smtp_server.lower() and "(-1, b'\\x00\\x00\\x00')" in error_msg:
                # QQ邮箱特殊情况：显示错误但邮件已发送成功
                self.logger.info(f"通知邮件发送成功: {subject}")
                return
            
            if "gmail" in self.smtp_server.lower():
                if "Application-specific password required" in error_msg:
                    self.logger.error("Gmail需要使用应用专用密码，请访问 https://myaccount.google.com/apppasswords 生成")
                elif "Username and Password not accepted" in error_msg:
                    self.logger.error("Gmail密码错误，请确保使用的是应用专用密码而不是普通密码")
            elif "qq" in self.smtp_server.lower():
                if "Connection unexpectedly closed" in error_msg:
                    self.logger.error("QQ邮箱连接失败，请确保：")
                    self.logger.error("1. 已在QQ邮箱设置中开启SMTP服务")
                    self.logger.error("2. 使用的是授权码而不是QQ密码")
                elif "Authentication failed" in error_msg:
                    self.logger.error("QQ邮箱认证失败，请确保使用的是授权码而不是QQ密码")
            elif "163" in self.smtp_server.lower():
                if "Authentication failed" in error_msg:
                    self.logger.error("163邮箱密码错误，请使用授权码而不是邮箱密码")
            else:
                if "Authentication failed" in error_msg:
                    self.logger.error(f"邮箱认证失败，请检查邮箱和密码是否正确")
                elif "Connection refused" in error_msg:
                    self.logger.error(f"无法连接到SMTP服务器 {self.smtp_server}:{self.smtp_port}")
                else:
                    self.logger.error(f"发送通知失败: {error_msg}")
            raise e
            
    def _check_email_config(self) -> bool:
        """检查邮件配置是否完整"""
        return bool(self.email and self.email_password) 