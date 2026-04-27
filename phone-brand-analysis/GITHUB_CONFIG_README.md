# GitHub 自动推送配置说明

## 配置步骤

### 1. 创建 GitHub Personal Access Token

1. 访问 GitHub：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 设置 token 名称：`coze-workflow-auto-push`
4. 选择权限：
   - `repo` (完整的仓库访问权限)
   - `workflow` (工作流权限)
5. 点击 "Generate token"
6. **复制 token**（只显示一次，请妥善保存）

### 2. 配置 Git

在你的项目目录中运行：

```bash
cd phone-brand-analysis

# 配置 Git 用户信息（如果还未配置）
git config user.name "你的用户名"
git config user.email "你的邮箱"

# 设置远程仓库（如果还未设置）
git remote add origin https://github.com/xhkdbukbushgjg/coze-1QAZBNDSAVFHK.git

# 验证远程仓库
git remote -v
```

### 3. 配置 Git 凭证

有两种方式：

#### 方式一：使用 Personal Access Token（推荐）

```bash
# 在推送时使用 token
git push https://<你的token>@github.com/xhkdbukbushgjg/coze-1QAZBNDSAVFHK.git main
```

#### 方式二：使用 Git Credential Manager

```bash
# 首次推送时会提示输入用户名和密码
# 用户名：你的 GitHub 用户名
# 密码：你的 Personal Access Token
```

### 4. 配置环境变量（可选）

如果需要在代码中配置，可以创建环境变量文件：

```bash
# 在项目根目录创建 .env 文件
echo "GITHUB_TOKEN=你的token" > .env
```

## 自动推送流程

工作流执行完成后，会自动：

1. ✅ 生成 Markdown 报告到 `reports/` 目录
2. ✅ 提交到 Git 仓库
3. ✅ 推送到 GitHub 远程仓库
4. ✅ 返回 GitHub 文件 URL

## 查看推送结果

### 方式一：查看日志

```bash
# 查看执行日志
cat logs/scheduler_$(date +%Y%m%d).log

# 查找 GitHub 推送相关信息
grep -i "github" logs/scheduler_$(date +%Y%m%d).log
```

### 方式二：查看 GitHub 仓库

直接访问：**https://github.com/xhkdbukbushgjg/coze-1QAZBNDSAVFHK**

查看 `reports/` 目录下的最新 Markdown 文件。

### 方式三：查看本地记录

```bash
# 查看结果记录
cat reports/result_$(date +%Y-%m-%d).txt
```

## 常见问题

### 1. 推送失败：认证错误

**错误信息**：`Authentication failed`

**解决方案**：
- 检查 Token 是否正确
- 确认 Token 有 `repo` 权限
- Token 可能已过期，需要重新生成

### 2. 推送失败：权限不足

**错误信息**：`Permission denied`

**解决方案**：
- 确认你有该仓库的写入权限
- 检查 Token 是否有正确的权限范围

### 3. 推送失败：分支冲突

**错误信息**：`Updates were rejected because the tip of your current branch is behind`

**解决方案**：

```bash
# 拉取最新代码
git pull origin main

# 如果有冲突，手动解决后再推送
git push origin main
```

### 4. 推送成功但找不到文件

**原因**：可能文件在子目录中

**解决方案**：
- 查看 `reports/` 目录
- 使用 GitHub 搜索功能查找文件

## 自动推送测试

手动测试自动推送功能：

```bash
cd phone-brand-analysis

# 运行完整工作流（包含 GitHub 推送）
python3 scripts/scheduler_full.py

# 查看日志确认推送是否成功
tail -f logs/scheduler_$(date +%Y%m%d).log
```

## 安全建议

1. **不要提交 Token 到代码库**：使用 `.gitignore` 排除 `.env` 文件
2. **定期更换 Token**：建议每 3-6 个月更换一次
3. **限制 Token 权限**：只授予必要的权限
4. **监控推送日志**：定期检查是否有异常推送

## .gitignore 配置

在项目根目录创建 `.gitignore` 文件：

```gitignore
# 环境变量
.env

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# 日志
logs/*.log
*.log

# 临时文件
*.tmp
.DS_Store
Thumbs.db
```
