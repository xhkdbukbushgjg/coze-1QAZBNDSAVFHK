# 手机品牌差评分析 - 完整自动化流程

## 🎯 项目概述

这是一个完全自动化的手机品牌差评分析工作流，能够：

- ✅ **每周自动运行**：定时任务自动执行
- ✅ **收集真实数据**：联网搜索 6 大品牌差评信息
- ✅ **生成专业报告**：8 章节结构化分析
- ✅ **自动推送到 GitHub**：报告自动提交到 GitHub 仓库
- ✅ **你只负责查看**：每周去 GitHub 查看结果

---

## 📋 完整工作流程

```
每周一上午 9:00
    ↓
📍 定时任务触发
    ↓
📍 收集品牌数据
    - 搜索苹果、华为、小米、OPPO、荣耀、vivo
    - 分类：通信/系统/硬件问题
    ↓
📍 生成分析报告
    - 使用大模型生成 Markdown 报告
    - 包含 8 个完整章节
    ↓
📍 生成 PDF 文档
    - 转换为 PDF 格式
    - 上传到对象存储
    - 保存 Markdown 到本地
    ↓
📍 推送到 GitHub
    - 自动提交到 Git 仓库
    - 推送到远程仓库
    - 返回 GitHub URL
    ↓
✅ 完成
    - 查看日志：logs/scheduler_YYYYMMDD.log
    - 查看 PDF：输出的 document_url
    - 查看 GitHub：https://github.com/xhkdbukbushgjg
```

---

## 🚀 快速开始

### 1. 配置 GitHub Token

按照 **[GITHUB_CONFIG_README.md](GITHUB_CONFIG_README.md)** 中的步骤配置 GitHub Token。

### 2. 设置定时任务

```bash
cd phone-brand-analysis

# 自动设置定时任务（每周一上午 9:00）
chmod +x scripts/setup_cron.sh
./scripts/setup_cron.sh

# 使用完整版脚本（包含 GitHub 推送）
crontab -e

# 添加以下内容（替换路径）
0 9 * * 1 cd /your/path/to/phone-brand-analysis && python3 scripts/scheduler_full.py >> logs/cron.log 2>&1
```

### 3. 测试运行

```bash
cd phone-brand-analysis

# 手动运行测试
python3 scripts/scheduler_full.py

# 查看日志
tail -f logs/scheduler_$(date +%Y%m%d).log
```

### 4. 查看结果

#### 查看日志
```bash
cat logs/scheduler_$(date +%Y%m%d).log
```

#### 查看 GitHub
访问：**https://github.com/xhkdbukbushgjg/coze-1QAZBNDSAVFHK**

查看 `reports/` 目录下的 Markdown 文件。

#### 查看本地记录
```bash
cat reports/result_$(date +%Y-%m-%d).txt
```

---

## 📊 每周查看流程

### 1. 打开 GitHub 仓库

访问：**https://github.com/xhkdbukbushgjg/coze-1QAZBNDSAVFHK**

### 2. 查看 `reports/` 目录

找到最新的 Markdown 报告文件，例如：
- `brand_analysis_report_20260427.md`
- `brand_analysis_report_20260505.md`

### 3. 查看报告内容

点击文件，直接在 GitHub 上查看 Markdown 格式的报告。

### 4. 下载 PDF（可选）

在执行日志中找到 `document_url`，点击链接下载 PDF 文件。

---

## 📁 项目结构

```
phone-brand-analysis/
├── reports/                          # 报告目录（自动推送到 GitHub）
│   ├── brand_analysis_report_20260427.md
│   ├── brand_analysis_report_20260505.md
│   └── result_2026-04-27.txt
├── logs/                             # 日志目录
│   ├── scheduler_20260427.log
│   └── cron.log
├── src/
│   ├── graphs/
│   │   ├── graph.py                  # 主图编排（包含 GitHub 推送）
│   │   ├── state.py                  # 状态定义
│   │   └── nodes/
│   │       ├── collect_all_brands_node.py
│   │       ├── search_brands_node.py
│   │       ├── generate_report_node.py
│   │       ├── generate_document_node.py
│   │       └── push_to_github_node.py  # GitHub 推送节点
│   └── ...
├── scripts/
│   ├── scheduler_full.py             # 完整定时任务脚本
│   ├── scheduler.py                  # 单次执行脚本
│   ├── continuous_scheduler.py       # 持续调度器
│   ├── setup_cron.sh                 # Cron 设置脚本
│   └── crontab.example               # Cron 配置示例
├── config/
│   └── generate_report_llm_cfg.json
├── README.md
├── SCHEDULER_README.md               # 定时任务详细说明
└── GITHUB_CONFIG_README.md           # GitHub 配置说明
```

---

## 🎉 你的工作流程

### 启动后，你只需要：

1. **等待周一**：每周一上午 9:00 自动运行
2. **查看 GitHub**：访问仓库查看本周报告
3. **阅读分析**：查看各品牌差评分析
4. **继续等待**：下周自动生成新报告

### 你不需要：

- ❌ 手动触发工作流
- ❌ 处理数据收集
- ❌ 生成报告
- ❌ 提交到 GitHub
- ❌ 管理定时任务

---

## 🔍 监控和维护

### 查看执行状态

```bash
# 查看 Cron 任务
crontab -l

# 查看最新日志
tail -f logs/cron.log
tail -f logs/scheduler_$(date +%Y%m%d).log

# 查看进程
ps aux | grep scheduler
```

### 手动触发执行

如果需要立即执行：

```bash
cd phone-brand-analysis
python3 scripts/scheduler_full.py
```

### 暂停自动执行

```bash
# 编辑 crontab
crontab -e

# 注释掉定时任务
# 0 9 * * 1 cd /your/path/to/phone-brand-analysis && python3 scripts/scheduler_full.py >> logs/cron.log 2>&1

# 保存退出
```

### 恢复自动执行

取消注释上面的定时任务配置即可。

---

## 📞 故障排查

### 问题：GitHub 推送失败

**查看日志**：
```bash
grep -i "github\|git" logs/scheduler_$(date +%Y%m%d).log
```

**解决方案**：
参考 **[GITHUB_CONFIG_README.md](GITHUB_CONFIG_README.md)** 中的常见问题。

### 问题：定时任务未执行

**检查 Cron 服务**：
```bash
sudo systemctl status cron
```

**查看 Cron 日志**：
```bash
tail -f logs/cron.log
```

### 问题：报告内容为空

**手动测试**：
```bash
cd phone-brand-analysis
python3 scripts/scheduler_full.py
```

查看详细日志定位问题。

---

## 📖 更多文档

- **[README.md](README.md)** - 项目基本信息
- **[SCHEDULER_README.md](SCHEDULER_README.md)** - 定时任务详细配置
- **[GITHUB_CONFIG_README.md](GITHUB_CONFIG_README.md)** - GitHub 配置说明
- **[AGENTS.md](AGENTS.md)** - 工作流节点说明

---

## ✨ 总结

**你现在的完整流程**：

1. **配置一次**：设置 GitHub Token 和定时任务
2. **每周自动**：系统自动运行、生成报告、推送到 GitHub
3. **每周查看**：去 GitHub 查看本周分析报告
4. **持续优化**：根据分析结果优化产品和策略

一切都自动化完成！🎉
