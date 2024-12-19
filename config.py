import json
import os
from typing import Dict

class Config:
    def __init__(self):
        self.config_data: Dict = self._load_config()
    
    def _load_config(self) -> Dict:
        # 优先使用环境变量
        if self._check_env_variables():
            return self._load_from_env()
        # 回退到本地配置文件
        return self._load_from_file()
    
    def _check_env_variables(self) -> bool:
        """检查必要的环境变量是否存在"""
        required_vars = ["MUSIC_U", "CSRF"]
        return all(os.getenv(var) for var in required_vars)
    
    def _load_from_env(self) -> Dict:
        """从环境变量加载配置"""
        return {
            "Cookie_MUSIC_U": os.getenv("MUSIC_U"),
            "Cookie___csrf": os.getenv("CSRF"),
            "notify_email": os.getenv("NOTIFY_EMAIL"),
            "email_password": os.getenv("EMAIL_PASSWORD"),
            "smtp_server": os.getenv("SMTP_SERVER"),
            "smtp_port": os.getenv("SMTP_PORT")
        }
    
    def _load_from_file(self) -> Dict:
        """从本地文件加载配置"""
        try:
            config_path = "setting.json"
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"配置文件 {config_path} 不存在")
                
            with open(config_path, "r", encoding="utf-8") as file:
                config = json.loads(file.read())
                
            # 验证必要的配置项
            required_keys = ["Cookie_MUSIC_U", "Cookie___csrf"]
            for key in required_keys:
                if not config.get(key):
                    raise ValueError(f"配置文件中缺少必要的配置项: {key}")
                    
            return config
        except Exception as e:
            raise RuntimeError(f"配置加载失败: {str(e)}")
    
    def get(self, key: str) -> str:
        value = self.config_data.get(key, "")
        if not value:
            raise ValueError(f"无法获取配置项: {key}")
        return value