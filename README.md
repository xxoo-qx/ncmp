# ncmp
A script repository for implementing music partner features of NetEase Cloud Music (网易云音乐).

## 功能特点

- 自动完成每日基础评分任务
- 自动完成额外评分任务
- 支持 GitHub Actions 自动运行
- 支持 Cookie 失效时自动发送邮件提醒

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

3. 配置文件设置：
进入项目根目录的 `setting.json` 文件，修改以下配置：
```json
{
  "Cookie_MUSIC_U": "YOUR_MUSIC_U_COOKIE_HERE",
  "Cookie___csrf": "YOUR_CSRF_TOKEN_HERE",
  "notify_email": "example@email.com",
  "email_password": "your_email_password",
  "smtp_server": "smtp.email.com",
  "smtp_port": 465
}
```

4. 运行脚本：
```bash
python main.py
```

### 方式二：GitHub Actions 自动执行

1. Fork 本仓库到你的 GitHub 账号

2. 配置 GitHub Secrets：
   在你 fork 的仓库中，进入 Settings -> Secrets and variables -> Actions，添加以下配置：
   - `MUSIC_U`：网易云音乐 MUSIC_U Cookie
   - `CSRF`：网易云音乐 CSRF Token
   - `NOTIFY_EMAIL`：通知邮箱（可选）
   - `EMAIL_PASSWORD`：邮箱密码（可选）
   - `SMTP_SERVER`：SMTP 服务器（可选）
   - `SMTP_PORT`：SMTP 端口（可选）

3. 启用 GitHub Actions：
   - 进入仓库的 Actions 页面
   - 点击 "I understand my workflows, go ahead and enable them"
   - Actions 将会按照预设时间自动运行（默认北京时间9点）

## 注意事项

- 请勿滥用本脚本
- 使用本脚本产生的任何后果由使用者自行承担
- 建议使用 GitHub Actions 的定时任务功能，避免遗漏每日任务
