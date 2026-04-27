#!/usr/bin/env python3
"""
持续运行的定时任务调度器
功能：使用 Python schedule 库实现定时任务，支持更灵活的调度策略
"""

import os
import sys
import time
import signal
import schedule
import logging
from datetime import datetime
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# 导入工作流运行函数
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from scheduler import run_workflow


def setup_logging():
    """配置日志"""
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"continuous_scheduler_{datetime.now().strftime('%Y%m%d')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


def job():
    """定时任务"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("触发定时任务")
    logger.info("=" * 60)

    try:
        success = run_workflow()
        if success:
            logger.info("✅ 定时任务执行成功")
        else:
            logger.error("❌ 定时任务执行失败")
    except Exception as e:
        logger.error(f"定时任务执行异常: {str(e)}", exc_info=True)


class GracefulExit:
    """优雅退出处理"""
    def __init__(self):
        self.shutdown = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.shutdown = True


def main():
    """主函数"""
    logger = setup_logging()
    logger.info("启动持续运行的定时任务调度器")
    logger.info("=" * 60)

    # 设置定时任务（每周一上午 9:00）
    schedule.every().monday.at("09:00").do(job)
    logger.info("已设置定时任务：每周一上午 9:00")

    # 可以添加更多定时任务
    # schedule.every().wednesday.at("09:00").do(job)
    # schedule.every().friday.at("09:00").do(job)

    logger.info("调度器正在运行，按 Ctrl+C 停止...")
    logger.info("=" * 60)

    graceful_exit = GracefulExit()

    try:
        while not graceful_exit.shutdown:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        pass

    logger.info("调度器已停止")


if __name__ == "__main__":
    main()
