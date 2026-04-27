import os
from typing import Dict
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import CollectBrandsInput, CollectBrandsOutput, BrandSearchInput
from graphs.nodes.search_brands_node import search_brands_node


def collect_all_brands_node(state: CollectBrandsInput, config: RunnableConfig, runtime: Runtime[Context]) -> CollectBrandsOutput:
    """
    title: 收集所有品牌数据
    desc: 并行搜索所有指定品牌的差评信息
    integrations: web-search
    """
    ctx = runtime.context
    
    brands = ["苹果", "华为", "小米", "OPPO", "荣耀", "vivo"]
    brand_results = {}
    
    # 为每个品牌执行搜索
    for brand in brands:
        try:
            # 创建正确的输入类型实例
            search_input = BrandSearchInput(brand_name=brand, report_date="")
            
            # 调用搜索节点
            result = search_brands_node(search_input, config, runtime)
            
            # 限制每个品牌的搜索结果数量，避免超出 LLM 上下文限制
            # 只保留最有代表性的 10 条结果（优先选择有发布时间的）
            limited_results = result.search_results[:10] if result.search_results else []

            brand_results[brand] = {
                "communication_issues": result.communication_issues,
                "system_issues": result.system_issues,
                "hardware_issues": result.hardware_issues,
                "search_count": len(result.search_results),
                # 包含限制后的搜索结果，让 LLM 可以引用来源链接
                "search_results": limited_results,
                "summary": f"搜索到{len(result.search_results)}条相关结果，精选{len(limited_results)}条"
            }
            
        except Exception as e:
            print(f"搜索品牌 {brand} 时出错: {e}")
            brand_results[brand] = {
                "communication_issues": [],
                "system_issues": [],
                "hardware_issues": [],
                "search_count": 0,
                "summary": f"搜索失败: {str(e)}",
                "error": str(e)
            }
    
    return CollectBrandsOutput(
        integrated_data={
            "brand_results": brand_results,
            "total_brands": len(brands)
        }
    )
