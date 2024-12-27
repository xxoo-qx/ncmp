import random
import time
import json
from typing import Dict, List, Tuple

class ExtraTask:
    def __init__(self, session, logger, config):
        self.session = session
        self.logger = logger
        self.config = config
        self.api = {
            "extra_list": "https://interface.music.163.com/api/music/partner/extra/wait/evaluate/work/list",
            "report_listen": "https://interface.music.163.com/weapi/partner/resource/interact/report"
        }
        # 从 Signer 类复用加密方法
        from signer import Signer
        self.signer = Signer(session, "", logger, config)  # task_id 为空字符串，因为上报听歌不需要

    def process_extra_tasks(self, task_id: str) -> None:
        """处理额外的评分任务"""
        try:
            extra_tasks, completed_count = self._get_extra_tasks()
            if not extra_tasks:
                self.logger.info(f"额外评定完成数: {completed_count}")
                return

            self.logger.info(f"发现 {len(extra_tasks)} 个待额外评定任务")
            for task in extra_tasks:
                self._process_single_task(task, task_id)
                # 添加随机等待时间
                delay = self.config.get_wait_time()
                self.logger.info(f"等待 {delay:.1f} 秒后继续...")
                time.sleep(delay)

        except Exception as e:
            self.logger.error(f"处理额外评分任务时出错: {str(e)}")
            raise

    def _get_extra_tasks(self) -> Tuple[List[Dict], int]:
        """获取额外评分任务列表"""
        try:
            response = self.session.get(
                url=self.api["extra_list"],
                headers={"Referer": "https://mp.music.163.com/"}
            ).json()

            if response["code"] != 200:
                raise RuntimeError(f"获取额外任务失败: {response.get('message', '未知错误')}")

            extra_tasks = response["data"]
            completed_tasks = [t for t in extra_tasks if t['completed']]
            uncompleted_tasks = [t for t in extra_tasks if not t['completed']]
            
            # 每天最多可以完成7个额外任务
            remaining_count = 7 - len(completed_tasks)
            available_tasks = uncompleted_tasks[:remaining_count] if remaining_count > 0 else []

            return available_tasks, len(completed_tasks)

        except Exception as e:
            self.logger.error(f"获取额外任务列表失败: {str(e)}")
            raise

    def _process_single_task(self, task: Dict, task_id: str) -> None:
        """处理单个额外评分任务"""
        work = task['work']
        try:
            # 1. 上报听歌记录
            self._report_listen(work)
            
            # 2. 评分
            from signer import Signer  # 复用现有的Signer类
            signer = Signer(self.session, task_id, self.logger)
            signer.sign(work, is_extra=True)

        except Exception as e:
            self.logger.error(f"处理额外任务失败 - {work['name']}: {str(e)}")
            raise

    def _report_listen(self, work: Dict) -> None:
        """上报听歌记录"""
        try:
            csrf = self.session.cookies["__csrf"]
            
            # 准备加密数据
            data = {
                "workId": work['id'],
                "resourceId": work['resourceId'],
                "bizResourceId": "",
                "interactType": "PLAY_END",
                "csrf_token": csrf
            }
            
            # 使用相同的加密方式
            params = {
                "params": self.signer._get_params(data),
                "encSecKey": self.signer._get_enc_sec_key()
            }
            
            response = self.session.post(
                url=f"{self.api['report_listen']}?csrf_token={csrf}",
                data=params,
                headers={"Referer": "https://mp.music.163.com/"}
            ).json()

            if response["code"] != 200:
                raise RuntimeError(f"上报听歌记录失败: {response.get('message', '未知错误')}")
            else:
                self.logger.info(f"歌曲 {work['name']} 听歌记录上报成功")

        except Exception as e:
            self.logger.error(f"上报听歌记录失败: {str(e)}")
            raise