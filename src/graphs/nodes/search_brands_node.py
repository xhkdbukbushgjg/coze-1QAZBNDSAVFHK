import os
import json
from typing import Dict, List
from datetime import datetime, timedelta, timezone
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from graphs.state import BrandSearchInput, BrandSearchOutput


def search_brands_node(state: BrandSearchInput, config: RunnableConfig, runtime: Runtime[Context]) -> BrandSearchOutput:
    """
    title: 品牌差评信息搜索
    desc: 搜索指定手机品牌的近期差评、用户吐槽、投诉等信息，并在代码层面筛选最近7天的数据
    integrations: web-search
    """
    ctx = runtime.context
    
    brand_name = state.brand_name
    report_date = state.report_date
    
    # 初始化搜索客户端
    client = SearchClient(ctx=ctx)
    
    # 计算时间筛选的截止日期（最近7天）
    # 使用带时区的 datetime，以便与搜索结果的 publish_time 进行比较
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)
    
    # 定义搜索关键词 - 覆盖不同类型的问题
    search_queries = [
        f"{brand_name} 差评 投诉",
        f"{brand_name} 信号差 通话问题",
        f"{brand_name} 发热 卡顿 闪退",
        f"{brand_name} 屏幕问题 电池",
        f"{brand_name} 系统更新 BUG",
        f"{brand_name} 用户吐槽",
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
            # 获取更多数据，不依赖 API 的时间筛选参数
            response = client.search(
                query=query,
                search_type="web",
                count=30,  # 增加搜索结果数量，以便代码层面筛选
                need_summary=True
            )
            
            if response.web_items:
                for item in response.web_items:
                    # 代码层面时间筛选：只保留最近7天的数据
                    is_within_week = False
                    
                    if item.publish_time:
                        try:
                            # 解析发布时间
                            publish_time = datetime.fromisoformat(item.publish_time.replace('Z', '+00:00'))
                            # 只保留最近7天的数据
                            if publish_time >= cutoff_date:
                                is_within_week = True
                        except Exception as e:
                            # 时间解析失败，跳过这条结果
                            print(f"⚠️ 时间解析失败: {item.publish_time}, 错误: {e}")
                            continue
                    else:
                        # 没有发布时间，跳过这条结果
                        continue
                    
                    if not is_within_week:
                        continue
                    
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
    
    # 限制返回数量，避免数据过多
    communication_issues = communication_issues[:10]
    system_issues = system_issues[:10]
    hardware_issues = hardware_issues[:10]
    
    # 限制原始内容长度，只保留关键信息
    raw_content = "\n".join(raw_content_list[:50])
    
    print(f"✅ 品牌 {brand_name}：搜索到 {len(all_results)} 条最近7天的结果")
    
    return BrandSearchOutput(
        brand_name=brand_name,
        search_results=all_results,
        communication_issues=communication_issues,
        system_issues=system_issues,
        hardware_issues=hardware_issues,
        raw_content=raw_content
    )
