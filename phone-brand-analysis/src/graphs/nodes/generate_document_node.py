import os
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import DocumentGenerationClient
from graphs.state import DocumentGenerationInput, DocumentGenerationOutput


def generate_document_node(state: DocumentGenerationInput, config: RunnableConfig, runtime: Runtime[Context]) -> DocumentGenerationOutput:
    """
    title: 生成分析报告文档
    desc: 将Markdown报告转换为PDF/DOCX文档并上传到对象存储
    integrations: document-generation
    """
    ctx = runtime.context
    
    markdown_report = state.markdown_report
    report_date = state.report_date
    
    # 初始化文档生成客户端
    doc_client = DocumentGenerationClient()
    
    # 生成文档标题（使用英文，避免中文路径问题）
    if report_date:
        date_str = report_date.replace("-", "")
    else:
        date_str = datetime.now().strftime("%Y%m%d")
    
    title = f"phone_brand_analysis_report_{date_str}"
    
    try:
        # 生成PDF文档
        document_url = doc_client.create_pdf_from_markdown(
            markdown_content=markdown_report,
            title=title
        )
        
    except Exception as e:
        print(f"生成PDF文档时出错: {e}")
        raise e
    
    return DocumentGenerationOutput(
        document_url=document_url
    )
