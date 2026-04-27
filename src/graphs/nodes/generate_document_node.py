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
    desc: 将Markdown报告转换为PDF文档并上传到对象存储，同时保存 Markdown 到本地
    integrations: document-generation
    """
    ctx = runtime.context
    
    markdown_report = state.markdown_report
    report_date = state.report_date
    
    # 确定报告日期
    if not report_date:
        report_date = datetime.now().strftime("%Y-%m-%d")
    
    # 项目根目录
    project_root = os.getenv("COZE_WORKSPACE_PATH", "/app")
    
    # 检测运行环境并选择合适的目录
    # API 环境使用临时目录，本地环境使用项目目录
    # 检测逻辑：不是本地路径就认为是 API 环境
    is_api_env = (
        project_root.startswith("/opt/") or
        not project_root.startswith("/workspace/")
    )
    
    if is_api_env:
        reports_dir = "/tmp/reports"
    else:
        reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    filename = f"brand_analysis_report_{report_date.replace('-', '')}.md"
    local_file_path = os.path.join(reports_dir, filename)
    
    with open(local_file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    print(f"✅ Markdown 文件已保存到本地: {local_file_path}")
    
    # 初始化文档生成客户端
    doc_client = DocumentGenerationClient()
    
    # 生成文档标题（使用英文，避免中文路径问题）
    date_str = report_date.replace("-", "")
    title = f"phone_brand_analysis_report_{date_str}"
    
    try:
        # 生成PDF文档
        document_url = doc_client.create_pdf_from_markdown(
            markdown_content=markdown_report,
            title=title
        )
        print(f"✅ PDF 文档已生成并上传到 S3")
        
    except Exception as e:
        print(f"生成PDF文档时出错: {e}")
        raise e
    
    return DocumentGenerationOutput(
        document_url=document_url
    )
