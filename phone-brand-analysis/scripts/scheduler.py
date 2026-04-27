#!/usr/bin/env python3
"""
手机品牌差评分析定时任务脚本
功能：每周自动运行一次工作流，生成分析报告
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# 添加项目路径到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from main import main


def setup_logging():
    """配置日志"""
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"scheduler_{datetime.now().strftime('%Y%m%d')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


def run_workflow():
    """运行工作流"""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("开始执行手机品牌差评分析任务")
    logger.info("=" * 60)

    try:
        # 准备输入参数
        current_date = datetime.now().strftime("%Y-%m-%d")
        input_data = {
            "report_date": current_date
        }

        logger.info(f"任务日期: {current_date}")
        logger.info(f"输入参数: {json.dumps(input_data, ensure_ascii=False)}")

        # 调用工作流
        logger.info("正在执行工作流...")
        result = main(mode="flow", input_json=json.dumps(input_data, ensure_ascii=False))

        logger.info("工作流执行成功！")
        logger.info(f"执行结果: {json.dumps(result, ensure_ascii=False, indent=2)}")

        # 提取并保存文档URL
        if result and isinstance(result, dict) and "document_url" in result:
            document_url = result["document_url"]
            logger.info(f"报告文档URL: {document_url}")

            # 保存URL到文件
            url_file = PROJECT_ROOT / "reports" / f"report_url_{current_date}.txt"
            url_file.parent.mkdir(exist_ok=True)
            with open(url_file, 'w', encoding='utf-8') as f:
                f.write(f"生成日期: {current_date}\n")
                f.write(f"文档URL: {document_url}\n")
                f.write(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            logger.info(f"文档URL已保存到: {url_file}")

        logger.info("=" * 60)
        logger.info("任务执行完成！")
        logger.info("=" * 60)
        return True

    except Exception as e:
        logger.error(f"工作流执行失败: {str(e)}", exc_info=True)
        logger.error("=" * 60)
        logger.error("任务执行失败！")
        logger.error("=" * 60)
        return False


def main_scheduler():
    """主函数"""
    success = run_workflow()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main_scheduler()
