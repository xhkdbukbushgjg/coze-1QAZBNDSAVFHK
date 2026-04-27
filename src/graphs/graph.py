from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)

from graphs.nodes.collect_all_brands_node import collect_all_brands_node
from graphs.nodes.generate_report_node import generate_report_node
from graphs.nodes.generate_document_node import generate_document_node


# 创建状态图，指定工作流的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("collect_brands", collect_all_brands_node)
builder.add_node("generate_report", generate_report_node, metadata={"type": "agent", "llm_cfg": "config/generate_report_llm_cfg.json"})
builder.add_node("generate_document", generate_document_node)

# 设置入口点
builder.set_entry_point("collect_brands")

# 添加边（线性流程）
builder.add_edge("collect_brands", "generate_report")
builder.add_edge("generate_report", "generate_document")
builder.add_edge("generate_document", END)

# 编译图
main_graph = builder.compile()
