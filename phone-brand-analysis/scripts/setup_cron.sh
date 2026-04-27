#!/bin/bash

# 设置定时任务脚本
# 用途：将定时任务添加到系统 crontab

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 检查是否已存在定时任务
if crontab -l 2>/dev/null | grep -q "scheduler.py"; then
    echo "⚠️  检测到已存在的定时任务！"
    echo ""
    echo "当前定时任务："
    crontab -l 2>/dev/null | grep "scheduler.py"
    echo ""
    read -p "是否要覆盖现有任务？(y/N): " confirm

    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "取消设置。"
        exit 0
    fi

    # 删除现有任务
    crontab -l 2>/dev/null | grep -v "scheduler.py" | crontab -
    echo "已删除现有任务。"
fi

# 获取项目绝对路径
ABSOLUTE_PATH=$(cd "$PROJECT_ROOT" && pwd)

# 创建日志目录
mkdir -p "$PROJECT_ROOT/logs"

# 添加新定时任务（每周一上午 9:00）
(crontab -l 2>/dev/null; echo "0 9 * * 1 cd $ABSOLUTE_PATH && python3 scripts/scheduler.py >> logs/cron.log 2>&1") | crontab -

echo "✅ 定时任务设置成功！"
echo ""
echo "任务详情："
echo "- 执行时间：每周一上午 9:00"
echo "- 执行命令：cd $ABSOLUTE_PATH && python3 scripts/scheduler.py"
echo "- 日志文件：$ABSOLUTE_PATH/logs/cron.log"
echo ""
echo "当前所有 crontab 任务："
crontab -l
echo ""
echo "如需修改执行时间，请使用以下命令编辑 crontab："
echo "  crontab -e"
