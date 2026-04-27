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
    desc: 并行搜索所有指定品牌的差评信息，在代码层面筛选最近7天的数据
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
            
            # 调用搜索节点（已在 search_brands_node 中进行时间筛选）
            result = search_brands_node(search_input, config, runtime)
            
            # 简化搜索结果数据结构，只保留 LLM 需要的字段
            # 每个品牌最多保留 5 条结果，避免数据量过大
            simplified_results = []
            for item in result.search_results[:5]:
                simplified_results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "publish_time": item.get("publish_time", "")
                })
            
            brand_results[brand] = {
                "communication_issues": result.communication_issues,
                "system_issues": result.system_issues,
                "hardware_issues": result.hardware_issues,
                "search_count": len(result.search_results),
                # 简化后的搜索结果，只包含标题、链接、发布时间
                "search_results": simplified_results,
                "summary": f"搜索到{len(result.search_results)}条最近7天的结果，精选{len(simplified_results)}条"
            }
            
        except Exception as e:
            print(f"搜索品牌 {brand} 时出错: {e}")
            brand_results[brand] = {
                "communication_issues": [],
                "system_issues": [],
                "hardware_issues": [],
                "search_count": 0,
                "search_results": [],
                "summary": f"搜索失败: {str(e)}",
                "error": str(e)
            }
    
    return CollectBrandsOutput(
        integrated_data={
            "brand_results": brand_results,
            "total_brands": len(brands)
        }
    )
