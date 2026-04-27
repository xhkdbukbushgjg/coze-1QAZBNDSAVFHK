import os
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk.s3 import S3SyncStorage
from graphs.state import DocumentGenerationInput, DocumentGenerationOutput


def generate_document_node(state: DocumentGenerationInput, config: RunnableConfig, runtime: Runtime[Context]) -> DocumentGenerationOutput:
    """
    title: 生成分析报告
    desc: 将 Markdown 报告保存到本地并上传到对象存储，返回 Markdown 文件的访问 URL
    integrations: storage
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
    
    # 构建文件名
    filename = f"brand_analysis_report_{report_date.replace('-', '')}.md"
    file_path = os.path.join(reports_dir, filename)
    
    # 写入 Markdown 文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    print(f"✅ Markdown 文件已保存到本地: {file_path}")
    
    # 上传 Markdown 文件到 S3 对象存储
    try:
        storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
        
        # 上传 Markdown 文件
        file_key = storage.upload_file(
            file_content=markdown_report.encode('utf-8'),
            file_name=f"reports/{filename}",
            content_type="text/markdown; charset=utf-8"
        )
        
        # 生成预签名 URL（有效期 24 小时）
        document_url = storage.generate_presigned_url(
            key=file_key,
            expire_time=86400  # 24 小时
        )
        
        print(f"✅ Markdown 文件已上传到 S3")
        print(f"📄 文件访问 URL: {document_url}")
        
    except Exception as e:
        print(f"❌ 上传 S3 失败: {str(e)}")
        # 如果 S3 上传失败，返回本地文件路径作为 fallback
        document_url = f"file://{file_path}"
    
    return DocumentGenerationOutput(
        document_url=document_url,
        report_date=report_date
    )
