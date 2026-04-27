# 手机品牌差评分析日报生成工作流

## 项目简介
这是一个自动化工作流，用于收集和分析主流手机品牌的用户差评信息，生成专业的分析报告。

## 功能特性
- ✅ 自动联网搜索6大手机品牌（苹果、华为、小米、OPPO、荣耀、vivo）的差评信息
- ✅ 智能分类问题（通信类/系统应用类/硬件品质类）
- ✅ 生成结构化的专业分析报告
- ✅ 输出PDF文档并上传到对象存储
- ⏰ 支持定时自动执行（每周/每天/自定义频率）

## 报告结构
1. 统计周期与生成日期
2. 数据来源说明
3. 整体数据概览
4. 各品牌详细分析
5. 跨品牌差异分析
6. 趋势总结
7. 需重点关注的问题
8. 数据局限性说明

## 快速开始

### 1. 安装依赖
```bash
cd phone-brand-analysis
uv sync
```

### 2. 手动运行
```bash
# 方式一：使用运行脚本
cd ..
bash scripts/local_run.sh -m flow

# 方式二：直接运行 Python
cd phone-brand-analysis
python3 scripts/scheduler.py
```

### 3. 设置定时任务（推荐）

#### 使用 Cron 定时任务（最简单）
```bash
cd phone-brand-analysis
chmod +x scripts/setup_cron.sh
./scripts/setup_cron.sh
```

默认设置为：**每周一上午 9:00** 自动执行。

#### 使用 Python 持续调度器（便于调试）
```bash
cd phone-brand-analysis
python3 scripts/continuous_scheduler.py
```

## 定时任务配置

详细的定时任务配置说明，请查看 **[SCHEDULER_README.md](SCHEDULER_README.md)**

### 快速配置示例

**每周一执行：**
```bash
0 9 * * 1 cd /path/to/phone-brand-analysis && python3 scripts/scheduler.py
```

**每周一、三、五执行：**
```bash
0 9 * * 1,3,5 cd /path/to/phone-brand-analysis && python3 scripts/scheduler.py
```

**每天执行：**
```bash
0 8 * * * cd /path/to/phone-brand-analysis && python3 scripts/scheduler.py
```

## 技术栈
- LangGraph 工作流编排
- Web Search 联网搜索
- 大语言模型（豆包-Seed-2.0-Pro）
- Document Generation 文档生成

## 项目结构
```
.
├── config/                 # 配置文件
│   └── generate_report_llm_cfg.json
├── scripts/                # 脚本文件
│   ├── scheduler.py                  # 定时任务脚本（单次执行）
│   ├── continuous_scheduler.py       # 持续运行调度器
│   ├── setup_cron.sh                 # Cron 设置脚本
│   └── crontab.example               # Crontab 配置示例
├── src/
│   ├── graphs/            # 工作流定义
│   │   ├── state.py      # 状态定义
│   │   ├── graph.py      # 主图编排
│   │   └── nodes/        # 节点实现
│   └── ...               # 其他源代码
├── logs/                  # 日志文件目录
├── reports/               # 报告文件目录
├── AGENTS.md              # 项目文档
├── SCHEDULER_README.md    # 定时任务详细说明
├── pyproject.toml         # 项目配置
└── README.md              # 本文件
```

## 查看执行结果

### 查看日志
```bash
# 查看任务执行日志
ls -la logs/
tail -f logs/scheduler_$(date +%Y%m%d).log

# 查看 cron 日志
tail -f logs/cron.log
```

### 查看报告 URL
```bash
# 查看最新生成的报告 URL
cat reports/report_url_$(date +%Y-%m-%d).txt

# 查看所有历史报告
ls -la reports/
```

## 监控和管理

### Cron 任务管理
```bash
# 查看当前所有 crontab 任务
crontab -l

# 编辑 crontab 任务
crontab -e

# 删除所有 crontab 任务
crontab -r
```

### 持续调度器管理
```bash
# 前台运行
python3 scripts/continuous_scheduler.py

# 后台运行
nohup python3 scripts/continuous_scheduler.py > logs/scheduler_daemon.log 2>&1 &

# 查看进程
ps aux | grep continuous_scheduler

# 停止进程
kill <PID>
```

## 故障排查

如果定时任务未正常执行，请检查：
1. 脚本是否有执行权限：`chmod +x scripts/scheduler.py`
2. Python 环境是否正确
3. 日志文件是否可写：`ls -la logs/`
4. Cron 服务是否运行：`sudo systemctl status cron`

详细的故障排查请参考 **[SCHEDULER_README.md](SCHEDULER_README.md)**

## License
MIT

