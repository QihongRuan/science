# 🚀 Claude Code 设置指南（中文版）

## 概述
本指南将帮助您使用共享的 API 密钥设置 Claude Code，以便与合作伙伴协作进行 AI 辅助编程。

---

## 📋 前置要求

### 系统要求
- **操作系统**：Windows 10+、macOS 10.15+ 或 Linux
- **Node.js**：18.0 或更高版本（用于 npm 安装）
- **存储空间**：至少 500MB 可用空间
- **网络**：稳定的互联网连接

### 需要准备的内容
- **Anthropic API 密钥**（由您的合作伙伴提供）
- **终端/命令提示符**访问权限
- **文本编辑器**（用于编辑配置文件）

---

## 🔧 安装方法

### 方法 1：全局 npm 安装（推荐）
```bash
# 通过 npm 全局安装 Claude Code
npm install -g @anthropic/claude-code

# 验证安装
claude --version
```

### 方法 2：原生二进制安装（测试版）
```bash
# macOS/Linux
curl -fsSL https://claudecode.ai/install.sh | sh

# Windows（以管理员身份运行 PowerShell）
irm https://claudecode.ai/install.ps1 | iex
```

### 方法 3：项目本地安装
```bash
# 在项目目录中
npm install @anthropic/claude-code --save-dev

# 本地运行
npx claude
```

---

## 🔑 API 密钥配置

### 方法 1：环境变量（最安全）

#### macOS/Linux：
```bash
# 添加到 ~/.bashrc、~/.zshrc 或 ~/.bash_profile
export ANTHROPIC_API_KEY="sk-ant-api03-您的密钥"

# 重新加载配置
source ~/.bashrc  # 或 ~/.zshrc
```

#### Windows：
```powershell
# PowerShell（永久设置）
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY','sk-ant-api03-您的密钥','User')

# 或命令提示符（临时设置）
set ANTHROPIC_API_KEY=sk-ant-api03-您的密钥
```

### 方法 2：Claude 配置文件

```bash
# 初始化 Claude 配置
claude config init

# 设置 API 密钥
claude config set api-key sk-ant-api03-您的密钥

# 验证配置
claude config list
```

### 方法 3：项目级配置

在项目根目录创建 `.claude/settings.json`：
```json
{
  "apiKey": "sk-ant-api03-您的密钥",
  "model": "claude-3-opus-20240229",
  "maxTokens": 4096,
  "temperature": 0.7
}
```

**⚠️ 重要**：将 `.claude/` 添加到 `.gitignore` 防止提交密钥：
```bash
echo ".claude/" >> .gitignore
```

---

## 🚀 开始使用

### 1. 验证设置
```bash
# 测试连接
claude test

# 或启动交互式会话
claude chat "你好，能帮我写代码吗？"
```

### 2. 基本命令
```bash
# 在当前目录启动 Claude Code
claude

# 打开特定项目
claude /path/to/project

# 使用特定模型
claude --model opus

# 获取帮助
claude --help
```

### 3. VS Code 集成（可选）
```bash
# 安装 VS Code 扩展
code --install-extension anthropic.claude-code

# 在 VS Code 设置中配置
# Cmd/Ctrl + Shift + P -> "Claude: Configure API Key"
```

---

## 🔒 安全最佳实践

### 应该做的 ✅
- **将 API 密钥存储在环境变量**或安全配置文件中
- **尽可能使用项目专用密钥**
- **定期轮换密钥**（建议每月一次）
- **立即将 `.claude/` 添加到 `.gitignore`**
- **在共享项目中使用只读密钥**（如果可用）
- **在 Anthropic 控制台设置消费限制**

### 不应该做的 ❌
- **永远不要将 API 密钥提交到版本控制**
- **不要通过明文分享密钥**（邮件、聊天等）
- **避免在源代码中硬编码密钥**
- **不要在开发中使用生产密钥**
- **永远不要在问题或论坛中发布密钥**

---

## 🛠️ 故障排除

### 常见问题和解决方案

#### 1. "API 密钥无效"错误
```bash
# 检查密钥是否设置
echo $ANTHROPIC_API_KEY  # macOS/Linux
echo %ANTHROPIC_API_KEY% # Windows

# 重新配置
claude config set api-key 您的密钥
```

#### 2. "找不到命令"
```bash
# 检查安装
which claude  # macOS/Linux
where claude  # Windows

# 如需要，重新安装
npm uninstall -g @anthropic/claude-code
npm install -g @anthropic/claude-code
```

#### 3. "超出速率限制"
- 等待 1 分钟后重试
- 在 Anthropic 控制台检查 API 使用情况
- 如果经常达到限制，考虑升级计划

#### 4. "连接超时"
```bash
# 测试网络连接
ping api.anthropic.com

# 如需要，配置代理
export HTTPS_PROXY=http://proxy.company.com:8080
```

---

## 📊 使用监控

### 检查 API 使用情况
```bash
# 查看当前使用情况
claude usage

# 检查速率限制
claude limits
```

### 在 Anthropic 控制台监控
1. 访问 [console.anthropic.com](https://console.anthropic.com)
2. 导航到"使用情况"标签
3. 设置账单警报

---

## 🤝 协作提示

### 共享项目
1. **创建共享仓库**（GitHub/GitLab）
2. **使用环境变量**存储 API 密钥
3. **在项目 README 中记录设置**
4. **在 `.claude/settings.json` 中设置一致的 Claude Code 配置**

### 团队配置模板
```json
{
  "apiKey": "${ANTHROPIC_API_KEY}",
  "model": "claude-3-opus-20240229",
  "maxTokens": 4096,
  "temperature": 0.7,
  "teamPresets": {
    "代码审查": {
      "prompt": "审查此代码的错误和改进建议"
    },
    "重构": {
      "prompt": "按照最佳实践重构此代码"
    }
  }
}
```

---

## 📝 给合作伙伴的注意事项

### 分享 API 密钥时：
1. **安全发送**（使用密码管理器、加密消息或安全文件传输）
2. **包含速率限制信息**（如适用）
3. **指定允许的用途**（仅开发、特定项目等）
4. **设置过期时间**（如果是临时访问）

### 消息模板：
```
嗨 [合作伙伴]，

这是 Claude Code 的设置信息：

1. API 密钥：[安全发送 - 不要用明文]
2. 使用的模型：claude-3-opus-20240229
3. 速率限制：每天 1000 个请求
4. 有效期至：[日期]

请按照设置指南操作：CLAUDE_CODE_设置指南.md
不要将 API 密钥提交到 git！

如有任何问题请告诉我。
```

---

## ✅ 设置清单

- [ ] 满足系统要求
- [ ] 已安装 Claude Code
- [ ] 已配置 API 密钥
- [ ] 已设置环境变量
- [ ] 已更新 `.gitignore`
- [ ] 已测试连接
- [ ] 已安装 VS Code 扩展（可选）
- [ ] 已配置团队设置
- [ ] 已查看文档

---

## 🚨 快速设置脚本

保存为 `setup-claude.sh`（macOS/Linux）或 `setup-claude.ps1`（Windows）：

### macOS/Linux：
```bash
#!/bin/bash
echo "🚀 正在设置 Claude Code..."

# 通过 npm 安装
npm install -g @anthropic/claude-code

# 获取 API 密钥
read -s -p "请输入您的 Anthropic API 密钥: " API_KEY
echo

# 设置环境变量
echo "export ANTHROPIC_API_KEY='$API_KEY'" >> ~/.bashrc
source ~/.bashrc

# 测试连接
claude test

echo "✅ Claude Code 设置完成！"
```

### Windows PowerShell：
```powershell
Write-Host "🚀 正在设置 Claude Code..." -ForegroundColor Green

# 通过 npm 安装
npm install -g @anthropic/claude-code

# 获取 API 密钥
$apiKey = Read-Host "请输入您的 Anthropic API 密钥" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey)
$key = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# 设置环境变量
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', $key, 'User')

# 测试连接
claude test

Write-Host "✅ Claude Code 设置完成！" -ForegroundColor Green
```

---

## 🆘 获取帮助

### 如果遇到问题：
1. 查看本指南的故障排除部分
2. 运行 `claude doctor` 进行诊断
3. 访问 [Claude Code Issues](https://github.com/anthropics/claude-code/issues)
4. 联系 Anthropic 支持
5. 向您的合作伙伴寻求帮助

---

## 📚 有用资源

### 官方文档
- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [API 参考](https://docs.anthropic.com/api)
- [最佳实践](https://docs.anthropic.com/best-practices)

### 命令参考
```bash
claude --help              # 通用帮助
claude chat               # 启动聊天会话
claude code              # 代码专用模式
claude review <文件>      # 审查代码文件
claude test              # 测试连接
claude config            # 配置管理
claude usage             # 检查 API 使用情况
claude update            # 更新 Claude Code
```

---

*最后更新：2024 年 12 月*
*Claude Code 版本：最新*

**记住**：保护好您的 API 密钥，永远不要公开分享！🔐