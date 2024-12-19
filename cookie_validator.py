import requests
from typing import Tuple

class CookieValidator:
    def __init__(self, session, logger):
        self.session = session
        self.logger = logger
        self.check_urls = {
            "user_info": "https://music.163.com/api/nuser/account/get",
            "task_data": "https://interface.music.163.com/api/music/partner/daily/task/get"
        }

    def validate(self) -> Tuple[bool, str]:
        """验证Cookie是否有效"""
        try:
            # 检查用户信息
            user_response = self.session.get(self.check_urls["user_info"]).json()
            if user_response.get("code") == 301:
                return False, "Cookie已失效，请更新Cookie"
            
            # 检查任务访问权限
            task_response = self.session.get(self.check_urls["task_data"]).json()
            if task_response.get("code") == 301:
                return False, "Cookie已失效，请更新Cookie"
            
            # 检查是否有音乐合伙人权限
            if task_response.get("code") != 200:
                return False, "当前账号可能没有音乐��伙人权限"
            
            return True, "Cookie有效"
            
        except Exception as e:
            return False, f"Cookie验证失败: {str(e)}" 