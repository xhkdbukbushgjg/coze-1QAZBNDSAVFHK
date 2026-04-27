import os
import json
from typing import Dict, List
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from graphs.state import BrandSearchInput, BrandSearchOutput


def search_brands_node(state: BrandSearchInput, config: RunnableConfig, runtime: Runtime[Context]) -> BrandSearchOutput:
    """
    title: 品牌差评信息搜索
    desc: 搜索指定手机品牌的近期差评、用户吐槽、投诉等信息
    integrations: web-search
    """
    ctx = runtime.context
    
    brand_name = state.brand_name
    report_date = state.report_date
    
    # 初始化搜索客户端
    client = SearchClient(ctx=ctx)
    
    # 定义搜索关键词 - 覆盖不同类型的问题
    search_queries = [
        f"{brand_name} 差评 投诉 问题 1天",
        f"{brand_name} 信号差 通话问题 1天",
        f"{brand_name} 发热 卡顿 闪退 1天",
        f"{brand_name} 屏幕问题 电池 1天",
        f"{brand_name} 系统更新 BUG 1天",
        f"{brand_name} 用户吐槽 1天",
    ]
    
    # 存储所有搜索结果
    all_results = []
    communication_issues = []
    system_issues = []
    hardware_issues = []
    raw_content_list = []
    
    # 执行搜索
    for query in search_queries:
        try:
            response = client.search(
                query=query,
                search_type="web",
                count=10,
                time_range="1d",
                need_summary=True
            )
            
            if response.web_items:
                for item in response.web_items:
                    result_item = {
                        "title": item.title,
                        "url": item.url,
                        "snippet": item.snippet,
                        "summary": item.summary if item.summary else "",
                        "site_name": item.site_name,
                        "publish_time": item.publish_time
                    }
                    all_results.append(result_item)
                    raw_content_list.append(f"【{item.site_name}】{item.title}\n{item.snippet}\n{item.summary if item.summary else ''}\n")
                    
                    # 分类问题
                    text_content = (item.title + " " + item.snippet + " " + (item.summary or "")).lower()
                    
                    # 通信类问题
                    comm_keywords = ["信号", "wifi", "4g", "5g", "断流", "通话", "蓝牙", "nfc", "gps", "定位", "网络"]
                    if any(keyword in text_content for keyword in comm_keywords):
                        issue_desc = f"{item.title}（{item.site_name}）"
                        if issue_desc not in communication_issues:
                            communication_issues.append(issue_desc)
                    
                    # 系统与应用类问题
                    sys_keywords = ["发热", "卡顿", "闪退", "杀后台", "更新", "续航", "bug", "功能异常", "应用"]
                    if any(keyword in text_content for keyword in sys_keywords):
                        issue_desc = f"{item.title}（{item.site_name}）"
                        if issue_desc not in system_issues:
                            system_issues.append(issue_desc)
                    
                    # 硬件品质类问题
                    hw_keywords = ["屏幕", "绿线", "漏液", "花屏", "电池", "铰链", "结构件", "拍照", "影像", "喇叭", "充电", "摄像头"]
                    if any(keyword in text_content for keyword in hw_keywords):
                        issue_desc = f"{item.title}（{item.site_name}）"
                        if issue_desc not in hardware_issues:
                            hardware_issues.append(issue_desc)
                            
        except Exception as e:
            # 记录错误但继续执行
            print(f"搜索 '{query}' 时出错: {e}")
            continue
    
    # 合并所有原始内容
    raw_content = "\n".join(raw_content_list)
    
    # 限制返回数量，避免数据过多
    communication_issues = communication_issues[:20]
    system_issues = system_issues[:20]
    hardware_issues = hardware_issues[:20]
    
    return BrandSearchOutput(
        brand_name=brand_name,
        search_results=all_results,
        communication_issues=communication_issues,
        system_issues=system_issues,
        hardware_issues=hardware_issues,
        raw_content=raw_content
    )
