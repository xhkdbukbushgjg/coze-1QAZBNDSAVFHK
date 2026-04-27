import os
import json
from typing import Dict
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from langchain_core.messages import SystemMessage, HumanMessage
from coze_coding_dev_sdk import LLMClient
from graphs.state import ReportGenerationInput, ReportGenerationOutput


def generate_report_node(state: ReportGenerationInput, config: RunnableConfig, runtime: Runtime[Context]) -> ReportGenerationOutput:
    """
    title: 生成分析报告
    desc: 使用LLM根据收集的品牌数据生成结构化的分析报告
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    integrated_data = state.integrated_data
    report_date = state.report_date
    
    # 从配置文件读取提示词
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        llm_cfg = json.load(fd)
    
    llm_config = llm_cfg.get("config", {})
    system_prompt = llm_cfg.get("sp", "")
    user_prompt = llm_cfg.get("up", "")
    
    # 准备用户提示词的变量
    from jinja2 import Template
    user_tpl = Template(user_prompt)
    user_prompt_content = user_tpl.render({
        "report_date": report_date or "今天",
        "integrated_data": json.dumps(integrated_data, ensure_ascii=False, indent=2)
    })
    
    # 初始化LLM客户端
    llm_client = LLMClient(ctx=ctx)
    
    # 构建消息
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt_content)
    ]
    
    # 调用大模型生成报告
    response = llm_client.invoke(
        messages=messages,
        model=llm_config.get("model", "doubao-seed-2-0-pro-260215"),
        temperature=llm_config.get("temperature", 0.3),
        max_completion_tokens=llm_config.get("max_completion_tokens", 8192)
    )
    
    # 获取响应内容
    if isinstance(response.content, str):
        markdown_report = response.content
    else:
        # 处理列表类型的响应
        markdown_report = str(response.content)
    
    return ReportGenerationOutput(
        markdown_report=markdown_report
    )
