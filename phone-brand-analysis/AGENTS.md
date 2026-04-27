## 项目概述
- **名称**: 手机品牌差评分析日报生成工作流
- **功能**: 联网搜索6大手机品牌（苹果、华为、小米、OPPO、荣耀、vivo）的近期差评信息，自动生成结构化的分析报告

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| collect_brands | `nodes/collect_all_brands_node.py` | task | 收集所有品牌的差评信息 | - | - |
| generate_report | `nodes/generate_report_node.py` | agent | 生成Markdown分析报告 | - | `config/generate_report_llm_cfg.json` |
| generate_document | `nodes/generate_document_node.py` | task | 生成PDF文档并上传S3 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

### 子图清单
无子图

## 技能使用
- 节点 `search_brands_node` 使用 web-search 技能进行联网搜索
- 节点 `generate_report_node` 使用 llm 技能（大语言模型）生成分析报告
- 节点 `generate_document_node` 使用 document-generation 技能生成PDF文档

## 工作流说明
1. **collect_brands节点**: 并行搜索6个手机品牌的差评信息（通信类、系统类、硬件类问题）
2. **generate_report节点**: 使用LLM根据收集的数据生成结构化的Markdown分析报告
3. **generate_document节点**: 将Markdown报告转换为PDF文档并上传到对象存储

## 输出说明
- 工作流输出为PDF文档的下载URL
- 文档包含以下章节：
  1. 统计周期与生成日期
  2. 数据来源说明
  3. 整体数据概览
  4. 各品牌详细分析
  5. 跨品牌差异分析
  6. 趋势总结
  7. 需重点关注的问题
  8. 数据局限性说明
