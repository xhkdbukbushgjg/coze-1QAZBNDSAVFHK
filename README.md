# Coze Coding Project

> 由 Coze Coding 智能助手生成的项目

## 项目简介

这是一个使用 LangChain 和 LangGraph 构建的智能 Agent 项目，专注于实现高效的自动化任务处理和智能决策。

## 技术栈

- **Python**: 核心开发语言
- **LangChain**: 大语言模型应用框架
- **LangGraph**: 状态管理和工作流编排
- **OpenAI**: 大语言模型服务

## 项目结构

```
.
├── config/                   # 配置文件目录
│   └── agent_llm_config.json # Agent LLM 配置
├── docs/                     # 项目文档
├── scripts/                  # 脚本和工具
├── assets/                   # 资源文件
├── tests/                    # 测试文件
├── src/                      # 源代码目录
│   ├── agents/              # Agent 实现
│   │   └── agent.py         # 主 Agent 代码
│   ├── storage/             # 存储层实现
│   ├── tools/               # 工具定义
│   └── utils/               # 工具函数
├── README.md                # 项目说明
├── pyproject.toml          # 项目依赖配置
└── uv.lock                  # 依赖锁定文件
```

## 快速开始

### 环境要求

- Python 3.9+
- uv (包管理工具)

### 安装依赖

```bash
uv sync
```

### 运行项目

```bash
python src/main.py
```

## 开发指南

### 创建新 Agent

在 `src/agents/agent.py` 中定义你的 Agent 逻辑：

```python
from langchain.agents import create_agent

def build_agent(ctx=None):
    # 初始化 LLM
    # 定义工具
    # 返回 Agent 实例
    pass
```

### 添加工具

在 `src/tools/` 目录下创建新工具：

```python
from langchain.tools import tool

@tool
def my_tool(param: str) -> str:
    """工具描述"""
    return "结果"
```

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_agent.py
```

## 配置说明

Agent 的 LLM 配置位于 `config/agent_llm_config.json`，包含：

- `model`: 使用的模型名称
- `temperature`: 温度参数
- `top_p`: Top-p 采样参数
- `max_completion_tokens`: 最大生成 token 数
- `system_prompt`: 系统提示词
- `tools`: 可用工具列表

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

*本项目由 [Coze Coding](https://coze.cn) 生成和维护*
