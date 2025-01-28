# ncmp

ncmp(NetEase Cloud Music Partner/网易云音乐合伙人)

基于 Python 的网易云音乐-音乐合伙人任务脚本，支持本地运行和 GitHub Actions 自动执行。

## 功能特点

- 全自动完成音乐合伙人日常任务
  - 完成每日5个基础任务
  - 完成每日7个额外评分任务
- 便捷的部署方式
  - 支持本地手动运行
  - 支持 GitHub Actions 自动执行
- 完善的通知机制
  - Cookie 失效自动发送邮件提醒

## 使用前准备

### 获取网易云音乐 Cookie

1. 登录[网易云音乐网页版](https://music.163.com/)
2. 打开浏览器开发者工具（F12）
3. 切换到 Network（网络）选项卡
4. 刷新页面，在请求中找到 cookie 中的 `MUSIC_U` 和 `__csrf` 值

### 配置邮箱通知（可选）

支持所有提供 SMTP 服务的邮箱，以下是常见邮箱的配置示例：

1. Gmail (推荐)

   ```json
   {
     "notify_email": "your.email@gmail.com",
     "email_password": "YOUR_APP_SPECIFIC_PASSWORD",
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 465
   }
   ```

   注意：Gmail 需要开启两步验证并使用应用专用密码

2. QQ邮箱

   ```json
   {
     "notify_email": "your_qq@qq.com",
     "email_password": "YOUR_AUTH_CODE",
     "smtp_server": "smtp.qq.com",
     "smtp_port": 465
   }
   ```

   注意：需要在QQ邮箱设置中开启SMTP服务并获取授权码

## 使用方法

### 方式一：本地手动执行

1. 克隆仓库到本地：

   ```bash
   git clone https://github.com/ACAne0320/ncmp.git
   cd ncmp
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 复制并编辑配置文件：

   ```bash
   cp config/setting.example.json config/setting.json
   ```

4. 编辑 `config/setting.json`，填写以下配置：

   ```json
   {
     "Cookie_MUSIC_U": "YOUR_MUSIC_U_COOKIE",
     "Cookie___csrf": "YOUR_CSRF_TOKEN",
     "notify_email": "your.email@gmail.com",
     "email_password": "YOUR_APP_SPECIFIC_PASSWORD",
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 465,
     "wait_time_min": 15,
     "wait_time_max": 20
   }
   ```

5. 运行测试脚本确认配置正确：

   ```bash
   python tests/test_run.py
   ```

6. 运行主程序：

   ```bash
   python main.py
   ```

### 方式二：GitHub Actions 自动执行

1. Fork 本仓库到你的 GitHub 账号

2. 配置 GitHub Secrets：
   在你 fork 的仓库中，进入 Settings -> Secrets and variables -> Actions，添加以下配置：
   - `MUSIC_U`：网易云音乐 MUSIC_U Cookie
   - `CSRF`：网易云音乐 CSRF Token
   - `NOTIFY_EMAIL`：邮箱地址（可选）
   - `EMAIL_PASSWORD`：邮箱密码（可选）
   - `SMTP_SERVER`：smtp.gmail.com（可选）
   - `SMTP_PORT`：465（可选）
   - `WAIT_TIME_MIN`：最小等待时间（可选，默认15）
   - `WAIT_TIME_MAX`：最大等待时间（可选，默认20）

3. 启用 GitHub Actions：
   - 进入仓库的 Actions 页面
   - 点击 "I understand my workflows, go ahead and enable them"
   - Actions 将会按照预设时间自动运行（默认北京时间1点）

## 注意事项

- 目前仅对 Gmail/QQ邮箱 进行了验证，其他邮箱可能需要自行测试
- 邮箱密码为授权码，而非邮箱登录密码
- 任务提交默认添加了 15-20 秒的等待时间，避免被检测异常
- 建议使用 GitHub Actions 的定时任务功能，避免遗漏每日任务
- 网易云音乐的 Cookie 两周左右就会过期，建议配置邮箱以便及时收到失效通知

## 声明

- 本项目仅供学习交流使用
- 不得用于商业用途
- 使用本脚本产生的一切后果由使用者自行承担

## 致谢

- [qinglong-sign](https://github.com/KotoriMinami/qinglong-sign)
- [CloudMusicBot](https://github.com/C20C01/CloudMusicBot)
