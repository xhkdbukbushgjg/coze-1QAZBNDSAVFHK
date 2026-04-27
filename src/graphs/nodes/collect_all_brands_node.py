import os
from typing import Dict
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import CollectBrandsInput, CollectBrandsOutput
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
            search_input = {
                "brand_name": brand,
                "report_date": ""
            }
            
            # 调用搜索节点
            result = search_brands_node(search_input, config, runtime)
            
            brand_results[brand] = {
                "communication_issues": result.communication_issues,
                "system_issues": result.system_issues,
                "hardware_issues": result.hardware_issues,
                "raw_content": result.raw_content,
                "search_count": len(result.search_results)
            }
            
        except Exception as e:
            print(f"搜索品牌 {brand} 时出错: {e}")
            brand_results[brand] = {
                "communication_issues": [],
                "system_issues": [],
                "hardware_issues": [],
                "raw_content": "",
                "search_count": 0,
                "error": str(e)
            }
    
    return CollectBrandsOutput(
        integrated_data={
            "brand_results": brand_results,
            "total_brands": len(brands)
        }
    )
