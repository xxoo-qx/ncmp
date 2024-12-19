# ncmp
A script repository for implementing music partner features of NetEase Cloud Music (网易云音乐).

## 功能特点

- 自动完成每日基础评分任务
- 自动完成额外评分任务
- 支持邮件通知功能
- 支持 GitHub Actions 自动运行
- Cookie 失效自动提醒

## 使用方法

### 1. 配置文件设置

在项目根目录创建 `setting.json` 文件，填入以下配置：

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

### 2. 环境要求

- Python 3.x
- 安装依赖：

```bash
pip install -r requirements.txt
```

### 3. 运行方式

#### 本地运行

```bash
python main.py
```

#### GitHub Actions 自动运行
1. Fork 本仓库
2. 在仓库的 Settings -> Secrets 中添加以下配置：
   - `MUSIC_U`: 网易云音乐 MUSIC_U Cookie
   - `CSRF`: 网易云音乐 CSRF Token
   - `NOTIFY_EMAIL`: 通知邮箱（可选）
   - `EMAIL_PASSWORD`: 邮箱密码（可选）
   - `SMTP_SERVER`: SMTP 服务器（可选）
   - `SMTP_PORT`: SMTP 端口（可选）

## 注意事项

- 请勿滥用本脚本
- 使用本脚本产生的任何后果由使用者自行承担
- 建议使用 GitHub Actions 的定时任务功能，避免遗漏每日任务
