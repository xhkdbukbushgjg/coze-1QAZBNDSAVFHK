from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime


# ==================== 全局状态 ====================
class GlobalState(BaseModel):
    """全局状态定义"""
    report_date: str = Field(default="", description="报告日期")
    brand_results: Dict = Field(default={}, description="各品牌搜索结果字典")
    integrated_data: Dict = Field(default={}, description="整合后的分析数据")
    markdown_report: str = Field(default="", description="生成的Markdown报告内容")
    document_url: str = Field(default="", description="最终文档的S3下载URL")


# ==================== 图输入输出 ====================
class GraphInput(BaseModel):
    """工作流输入"""
    report_date: Optional[str] = Field(default="", description="报告日期（格式：YYYY-MM-DD），默认为今天")


class GraphOutput(BaseModel):
    """工作流输出"""
    document_url: str = Field(..., description="生成的分析报告文档URL")
    report_date: str = Field(..., description="报告日期")


# ==================== 品牌搜索节点 ====================
class BrandSearchInput(BaseModel):
    """品牌搜索节点输入"""
    brand_name: str = Field(..., description="品牌名称（苹果、华为、小米、OPPO、荣耀、vivo）")
    report_date: str = Field(..., description="报告日期")


class BrandSearchOutput(BaseModel):
    """品牌搜索节点输出"""
    brand_name: str = Field(..., description="品牌名称")
    search_results: List[Dict] = Field(default=[], description="原始搜索结果列表")
    communication_issues: List[str] = Field(default=[], description="通信类问题汇总")
    system_issues: List[str] = Field(default=[], description="系统与应用类问题汇总")
    hardware_issues: List[str] = Field(default=[], description="硬件品质类问题汇总")
    raw_content: str = Field(default="", description="原始搜索内容的文本汇总")


# ==================== 收集所有品牌节点 ====================
class CollectBrandsInput(BaseModel):
    """收集所有品牌节点输入"""
    report_date: str = Field(default="", description="报告日期")


class CollectBrandsOutput(BaseModel):
    """收集所有品牌节点输出"""
    integrated_data: Dict = Field(..., description="整合后的完整分析数据")


# ==================== 数据整合节点 ====================
class DataIntegrationInput(BaseModel):
    """数据整合节点输入（已废弃，由CollectBrandsNode代替）"""
    brand_results: Dict = Field(..., description="各品牌的搜索结果字典")


class DataIntegrationOutput(BaseModel):
    """数据整合节点输出（已废弃）"""
    integrated_data: Dict = Field(..., description="整合后的完整分析数据")


# ==================== 报告生成节点 ====================
class ReportGenerationInput(BaseModel):
    """报告生成节点输入"""
    integrated_data: Dict = Field(..., description="整合后的分析数据")
    report_date: Optional[str] = Field(default="", description="报告日期")


class ReportGenerationOutput(BaseModel):
    """报告生成节点输出"""
    markdown_report: str = Field(..., description="生成的Markdown格式报告")


# ==================== 文档生成节点 ====================
class DocumentGenerationInput(BaseModel):
    """文档生成节点输入"""
    markdown_report: str = Field(..., description="Markdown格式报告内容")
    report_date: Optional[str] = Field(default="", description="报告日期")


class DocumentGenerationOutput(BaseModel):
    """文档生成节点输出"""
    document_url: str = Field(..., description="生成的文档S3下载URL")


# ==================== GitHub 推送节点 ====================
class PushToGitHubInput(BaseModel):
    """GitHub 推送节点输入"""
    markdown_report: str = Field(..., description="Markdown 报告内容")
    report_date: str = Field(default="", description="报告日期")


class PushToGitHubOutput(BaseModel):
    """GitHub 推送节点输出"""
    success: bool = Field(..., description="是否成功推送")
    commit_message: str = Field(..., description="Git 提交信息")
    file_path: str = Field(..., description="文件在 GitHub 仓库中的路径")
    github_url: str = Field(..., description="GitHub 文件 URL")
