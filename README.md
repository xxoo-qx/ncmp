# ncmp

ncmp(NetEase Cloud Music Partner) 网易云音乐合伙人
一个基于 Python 的网易云音乐-音乐合伙人任务脚本，支持本地运行和 GitHub Actions 自动执行。

## 功能特点

- 全自动完成音乐合伙人日常任务
  - 完成每日基础任务
  - 完成每日额外评分任务
- 便捷的部署方式
  - 支持本地手动运行
  - 支持 GitHub Actions 自动执行
- 完善的通知机制
  - Cookie 失效自动发送邮件提醒
  - 支持自定义 SMTP 服务器

## 使用前准备

### 获取网易云音乐 Cookie

1. 登录[网易云音乐网页版](https://music.163.com/)
2. 打开浏览器开发者工具（F12）
3. 切换到 Network（网络）选项卡
4. 刷新页面，在请求中找到 cookie 中的 `MUSIC_U` 和 `__csrf` 值

### 配置邮箱（可选）

如需开启邮件通知功能，需要：
1. 使用邮箱开启 SMTP 服务
2. 获取邮箱授权码（不是邮箱密码）
3. 记录 SMTP 服务器地址和端口

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

## 声明

- 本项目仅供学习交流使用
- 不得用于商业用途
- 使用本脚本产生的一切后果由使用者自行承担

## 致谢

- [qinglong-sign](https://github.com/KotoriMinami/qinglong-sign)
- [CloudMusicBot](https://github.com/C20C01/CloudMusicBot)
