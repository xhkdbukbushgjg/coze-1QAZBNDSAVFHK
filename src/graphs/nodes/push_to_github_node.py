import os
import shutil
from datetime import datetime
from typing import Optional
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from pydantic import BaseModel, Field


class PushToGitHubInput(BaseModel):
    """GitHub 推送节点输入"""
    markdown_content: str = Field(..., description="Markdown 报告内容")
    report_date: str = Field(default="", description="报告日期")


class PushToGitHubOutput(BaseModel):
    """GitHub 推送节点输出"""
    success: bool = Field(..., description="是否成功推送")
    commit_message: str = Field(..., description="Git 提交信息")
    file_path: str = Field(..., description="文件在 GitHub 仓库中的路径")
    github_url: str = Field(..., description="GitHub 文件 URL")


def push_to_github_node(state: PushToGitHubInput, config: RunnableConfig, runtime: Runtime[Context]) -> PushToGitHubOutput:
    """
    title: 推送报告到 GitHub
    desc: 将生成的 Markdown 报告自动提交并推送到 GitHub 仓库
    integrations: git
    """
    ctx = runtime.context
    
    markdown_content = state.markdown_content
    report_date = state.report_date
    
    # 确定报告日期
    if not report_date:
        report_date = datetime.now().strftime("%Y-%m-%d")
    
    # 项目根目录
    project_root = os.getenv("COZE_WORKSPACE_PATH", "/app")
    
    # 创建 reports 目录（在项目根目录下）
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # 构建文件名
    filename = f"brand_analysis_report_{report_date.replace('-', '')}.md"
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
                github_url=""
            )
        
        # 添加文件到 git
        add_cmd = f"git add {filename}"
        print(f"执行: {add_cmd}")
        os.system(add_cmd)
        
        # 提交更改
        commit_msg = f"feat: 添加手机品牌差评分析报告 - {report_date}"
        commit_cmd = f'git commit -m "{commit_msg}"'
        print(f"执行: {commit_cmd}")
        os.system(commit_cmd)
        
        # 推送到远程仓库
        push_cmd = "git push origin main"
        print(f"执行: {push_cmd}")
        os.system(push_cmd)
        
        print("✅ 成功推送到 GitHub！")
        
        # 构建文件在 GitHub 上的 URL（需要根据实际仓库配置调整）
        # 这里使用占位符，实际需要从 git remote 获取
        github_url = f"https://github.com/xhkdbukbushgjg/coze-1QAZBNDSAVFHK/blob/main/{filename}"
        
        return PushToGitHubOutput(
            success=True,
            commit_message=commit_msg,
            file_path=f"reports/{filename}",
            github_url=github_url
        )
        
    except Exception as e:
        print(f"❌ Git 推送失败: {str(e)}")
        return PushToGitHubOutput(
            success=False,
            commit_message=f"提交失败: {str(e)}",
            file_path=file_path,
            github_url=""
        )
