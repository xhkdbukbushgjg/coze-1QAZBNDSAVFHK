# 定时任务使用说明

## 方式一：使用 Cron 定时任务（推荐）

### 1. 安装定时任务

```bash
# 进入项目目录
cd phone-brand-analysis

# 运行设置脚本
chmod +x scripts/setup_cron.sh
./scripts/setup_cron.sh
```

### 2. 手动配置 Cron

如果需要自定义执行时间，可以手动编辑 crontab：

```bash
# 编辑 crontab
crontab -e

# 添加以下内容（记得替换路径）
0 9 * * 1 cd /your/path/to/phone-brand-analysis && python3 scripts/scheduler.py >> logs/cron.log 2>&1
```

### 3. Cron 时间格式说明

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-7, 0或7=周日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

### 4. 常用时间示例

```bash
# 每周一上午 9:00
0 9 * * 1

# 每周一、周三、周五上午 9:00
0 9 * * 1,3,5

# 每天上午 8:00
0 8 * * *

# 每月1号上午 10:00
0 10 1 * *

# 每工作日（周一到周五）下午 5:00
0 17 * * 1-5

# 每周日上午 11:59
59 11 * * 0
```

### 5. 查看和管理定时任务

```bash
# 查看当前所有 crontab 任务
crontab -l

# 删除所有 crontab 任务
crontab -r

# 编辑 crontab 任务
crontab -e
```

### 6. 查看日志

```bash
# 查看 cron 日志
tail -f logs/cron.log

# 查看任务执行日志
ls -la logs/
cat logs/scheduler_YYYYMMDD.log
```

---

## 方式二：使用 Python 持续调度器

### 1. 安装依赖

```bash
cd phone-brand-analysis
uv add schedule
```

### 2. 运行调度器

```bash
# 前台运行（用于测试）
python3 scripts/continuous_scheduler.py

# 后台运行（用于生产）
nohup python3 scripts/continuous_scheduler.py > logs/scheduler_daemon.log 2>&1 &

# 查看进程
ps aux | grep continuous_scheduler

# 停止进程
kill <PID>
```

### 3. 修改执行时间

编辑 `scripts/continuous_scheduler.py` 文件中的定时任务配置：

```python
# 每周一上午 9:00
schedule.every().monday.at("09:00").do(job)

# 添加更多定时任务
schedule.every().wednesday.at("09:00").do(job)
schedule.every().friday.at("09:00").do(job)
```

---

## 方式三：使用 systemd（Linux 系统）

### 1. 创建服务文件

```bash
sudo nano /etc/systemd/system/phone-brand-analysis.service
```

### 2. 服务文件内容

```ini
[Unit]
Description=Phone Brand Analysis Scheduler
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/phone-brand-analysis
ExecStart=/usr/bin/python3 /path/to/phone-brand-analysis/scripts/continuous_scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. 启用和启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable phone-brand-analysis.service
sudo systemctl start phone-brand-analysis.service

# 查看服务状态
sudo systemctl status phone-brand-analysis.service

# 查看服务日志
sudo journalctl -u phone-brand-analysis.service -f
```

### 4. 创建定时器（可选）

如果需要精确控制执行时间，可以创建定时器：

```bash
sudo nano /etc/systemd/system/phone-brand-analysis.timer
```

```ini
[Unit]
Description=Run phone brand analysis weekly

[Timer]
OnCalendar=Mon *-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl enable phone-brand-analysis.timer
sudo systemctl start phone-brand-analysis.timer
```

---

## 日志和监控

### 日志文件位置

- **Cron 日志**：`logs/cron.log`
- **任务执行日志**：`logs/scheduler_YYYYMMDD.log`
- **持续调度器日志**：`logs/continuous_scheduler_YYYYMMDD.log`
- **报告 URL 记录**：`reports/report_url_YYYY-MM-DD.txt`

### 监控执行结果

```bash
# 查看最近的执行结果
cat reports/report_url_$(date +%Y-%m-%d).txt

# 查看所有历史报告 URL
ls -la reports/
```

---

## 故障排查

### 1. Cron 任务未执行

```bash
# 检查 cron 服务状态
sudo systemctl status cron

# 检查 cron 日志
sudo grep CRON /var/log/syslog

# 手动测试脚本
cd /path/to/phone-brand-analysis
python3 scripts/scheduler.py
```

### 2. Python 环境问题

确保使用正确的 Python 环境：

```bash
# 使用虚拟环境
source .venv/bin/activate
cd /path/to/phone-brand-analysis
python3 scripts/scheduler.py
```

### 3. 权限问题

```bash
# 确保脚本有执行权限
chmod +x scripts/scheduler.py
chmod +x scripts/continuous_scheduler.py
chmod +x scripts/setup_cron.sh
```

---

## 推荐方案

- **生产环境**：使用 **Cron 定时任务**（简单、稳定、可靠）
- **开发/测试环境**：使用 **Python 持续调度器**（便于调试和测试）
- **企业级部署**：使用 **systemd 服务**（更好的进程管理）
