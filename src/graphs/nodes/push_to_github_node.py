import os
import shutil
import subprocess
from datetime import datetime
from typing import Optional
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from pydantic import BaseModel, Field

from graphs.state import PushToGitHubInput, PushToGitHubOutput


def push_to_github_node(state: PushToGitHubInput, config: RunnableConfig, runtime: Runtime[Context]) -> PushToGitHubOutput:
    """
    title: 推送报告到 GitHub
    desc: 将生成的 Markdown 报告自动提交并推送到 GitHub 仓库
    integrations: git
    """
    ctx = runtime.context
    
    markdown_content = state.markdown_report
    report_date = state.report_date
    document_url = state.document_url  # 接收 document_url
    
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
    
    # 文件保存路径（用于生成）
    file_path = os.path.join(reports_dir, filename)
    
    # 写入 Markdown 文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Markdown 文件已生成: {file_path}")
    
    # Git 提交和推送
    try:
        # 切换到项目根目录
        os.chdir(project_root)
        
        # 检查是否在 git 仓库中
        if not os.path.exists(".git"):
            print("❌ 错误：当前目录不是 Git 仓库")
            return PushToGitHubOutput(
                success=False,
                commit_message="未在 Git 仓库中",
                file_path=file_path,
                github_url="",
                report_date=report_date,
                document_url=document_url
            )
        
        # 如果在 API 环境中，需要将文件复制到 Git 仓库的 reports/ 目录
        if is_api_env:
            # Git 仓库中的 reports/ 目录
            git_reports_dir = os.path.join(project_root, "reports")
            git_file_path = os.path.join(git_reports_dir, filename)
            
            # 尝试创建目录并复制文件
            try:
                os.makedirs(git_reports_dir, exist_ok=True)
                shutil.copy(file_path, git_file_path)
                print(f"✅ 文件已复制到 Git 仓库: {git_file_path}")
            except Exception as e:
                print(f"❌ 无法在 Git 仓库目录创建文件: {str(e)}")
                return PushToGitHubOutput(
                    success=False,
                    commit_message=f"无法写入 Git 仓库: {str(e)}",
                    file_path=file_path,
                    github_url="",
                    report_date=report_date,
                    document_url=document_url
                )
        else:
            # 本地环境，文件已在正确的位置
            git_file_path = file_path
        
        # 添加文件到 git
        # 注意：文件在 reports/ 目录下，需要使用相对路径 reports/{filename}
        add_cmd = f"git add reports/{filename}"
        print(f"执行: {add_cmd}")
        result = subprocess.run(add_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ git add 失败: {result.stderr}")
            return PushToGitHubOutput(
                success=False,
                commit_message=f"git add 失败: {result.stderr}",
                file_path=f"reports/{filename}",
                github_url="",
                report_date=report_date,
                document_url=document_url
            )
        
        # 提交更改
        commit_msg = f"feat: 添加手机品牌差评分析报告 - {report_date}"
        commit_cmd = f'git commit -m "{commit_msg}"'
        print(f"执行: {commit_cmd}")
        result = subprocess.run(commit_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ git commit 失败: {result.stderr}")
            return PushToGitHubOutput(
                success=False,
                commit_message=f"git commit 失败: {result.stderr}",
                file_path=f"reports/{filename}",
                github_url="",
                report_date=report_date,
                document_url=document_url
            )
        
        # 推送到远程仓库
        push_cmd = "git push origin main"
        print(f"执行: {push_cmd}")
        result = subprocess.run(push_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ git push 失败: {result.stderr}")
            return PushToGitHubOutput(
                success=False,
                commit_message=f"git push 失败: {result.stderr}",
                file_path=f"reports/{filename}",
                github_url="",
                report_date=report_date,
                document_url=document_url
            )
        
        print("✅ 成功推送到 GitHub！")
        
        # 构建文件在 GitHub 上的 URL
        # 文件保存在 reports/ 目录下，所以 URL 需要包含 reports/ 路径
        github_url = f"https://github.com/xhkdbukbushgjg/coze-1QAZBNDSAVFHK/blob/main/reports/{filename}"
        
        return PushToGitHubOutput(
            success=True,
            commit_message=commit_msg,
            file_path=f"reports/{filename}",
            github_url=github_url,
            report_date=report_date,
            document_url=document_url
        )
        
    except Exception as e:
        print(f"❌ Git 推送失败: {str(e)}")
        return PushToGitHubOutput(
            success=False,
            commit_message=f"提交失败: {str(e)}",
            file_path=file_path,
            github_url="",
            report_date=report_date,
            document_url=document_url
        )
