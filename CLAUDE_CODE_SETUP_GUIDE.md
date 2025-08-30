# 🚀 Claude Code Setup Guide for Partners

## Overview
This guide will help you set up Claude Code using a shared API key so you can collaborate on projects with full AI-powered coding assistance.

---

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **Node.js**: Version 18.0 or higher (for npm installation)
- **Storage**: At least 500MB free space
- **Internet**: Stable connection for API calls

### What You'll Need
- **Anthropic API Key** (will be provided by your partner)
- **Terminal/Command Prompt** access
- **Text editor** for configuration files

---

## 🔧 Installation Methods

### Option 1: Global npm Installation (Recommended)
```bash
# Install Claude Code globally via npm
npm install -g @anthropic/claude-code

# Verify installation
claude --version
```

### Option 2: Native Binary Installation (Beta)
```bash
# macOS/Linux
curl -fsSL https://claudecode.ai/install.sh | sh

# Windows (PowerShell as Administrator)
irm https://claudecode.ai/install.ps1 | iex
```

### Option 3: Local Project Installation
```bash
# In your project directory
npm install @anthropic/claude-code --save-dev

# Run locally
npx claude
```

---

## 🔑 API Key Configuration

### Method 1: Environment Variable (Most Secure)

#### macOS/Linux:
```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.bash_profile
export ANTHROPIC_API_KEY="sk-ant-api03-YOUR-KEY-HERE"

# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc
```

#### Windows:
```powershell
# PowerShell (permanent)
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY','sk-ant-api03-YOUR-KEY-HERE','User')

# Or Command Prompt (temporary)
set ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE
```

### Method 2: Claude Config File

```bash
# Initialize Claude configuration
claude config init

# Set API key
claude config set api-key sk-ant-api03-YOUR-KEY-HERE

# Verify configuration
claude config list
```

### Method 3: Project-Level Configuration

Create `.claude/settings.json` in your project root:
```json
{
  "apiKey": "sk-ant-api03-YOUR-KEY-HERE",
  "model": "claude-3-opus-20240229",
  "maxTokens": 4096,
  "temperature": 0.7
}
```

**⚠️ Important**: Add `.claude/` to `.gitignore` to prevent committing API keys:
```bash
echo ".claude/" >> .gitignore
```

---

## 🚀 Getting Started

### 1. Verify Setup
```bash
# Test connection
claude test

# Or start interactive session
claude chat "Hello, can you help me code?"
```

### 2. Basic Commands
```bash
# Start Claude Code in current directory
claude

# Open specific project
claude /path/to/project

# Use specific model
claude --model opus

# Get help
claude --help
```

### 3. VS Code Integration (Optional)
```bash
# Install VS Code extension
code --install-extension anthropic.claude-code

# Configure in VS Code settings
# Cmd/Ctrl + Shift + P -> "Claude: Configure API Key"
```

---

## 🔒 Security Best Practices

### DO's ✅
- **Store API key in environment variables** or secure config files
- **Use project-specific keys** when possible
- **Rotate keys regularly** (monthly recommended)
- **Add `.claude/` to `.gitignore`** immediately
- **Use read-only keys** for shared projects when available
- **Set spending limits** in Anthropic Console

### DON'Ts ❌
- **Never commit API keys** to version control
- **Don't share keys** in plain text (email, chat, etc.)
- **Avoid hardcoding keys** in source code
- **Don't use production keys** for development
- **Never post keys** in issues or forums

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. "API Key Invalid" Error
```bash
# Check if key is set
echo $ANTHROPIC_API_KEY  # macOS/Linux
echo %ANTHROPIC_API_KEY% # Windows

# Re-configure
claude config set api-key YOUR-KEY
```

#### 2. "Command Not Found"
```bash
# Check installation
which claude  # macOS/Linux
where claude  # Windows

# Reinstall if needed
npm uninstall -g @anthropic/claude-code
npm install -g @anthropic/claude-code
```

#### 3. "Rate Limit Exceeded"
- Wait 1 minute and retry
- Check API usage in Anthropic Console
- Consider upgrading plan if hitting limits frequently

#### 4. "Connection Timeout"
```bash
# Test internet connection
ping api.anthropic.com

# Configure proxy if needed
export HTTPS_PROXY=http://proxy.company.com:8080
```

---

## 📊 Usage Monitoring

### Check API Usage
```bash
# View current usage
claude usage

# Check rate limits
claude limits
```

### Monitor in Anthropic Console
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Navigate to "Usage" tab
3. Set up billing alerts

---

## 🤝 Collaboration Tips

### Sharing Projects
1. **Create shared repository** (GitHub/GitLab)
2. **Use environment variables** for API keys
3. **Document setup** in project README
4. **Set consistent Claude Code settings** in `.claude/settings.json`

### Team Configuration Template
```json
{
  "apiKey": "${ANTHROPIC_API_KEY}",
  "model": "claude-3-opus-20240229",
  "maxTokens": 4096,
  "temperature": 0.7,
  "teamPresets": {
    "codeReview": {
      "prompt": "Review this code for bugs and improvements"
    },
    "refactor": {
      "prompt": "Refactor this code following best practices"
    }
  }
}
```

---

## 📚 Useful Resources

### Official Documentation
- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [API Reference](https://docs.anthropic.com/api)
- [Best Practices](https://docs.anthropic.com/best-practices)

### Commands Reference
```bash
claude --help              # General help
claude chat               # Start chat session
claude code              # Code-specific mode
claude review <file>     # Review code file
claude test              # Test connection
claude config            # Configuration management
claude usage             # Check API usage
claude update            # Update Claude Code
```

---

## 🚨 Quick Setup Script

Save this as `setup-claude.sh` (macOS/Linux) or `setup-claude.ps1` (Windows):

### macOS/Linux:
```bash
#!/bin/bash
echo "🚀 Setting up Claude Code..."

# Install via npm
npm install -g @anthropic/claude-code

# Get API key
read -s -p "Enter your Anthropic API key: " API_KEY
echo

# Set environment variable
echo "export ANTHROPIC_API_KEY='$API_KEY'" >> ~/.bashrc
source ~/.bashrc

# Test connection
claude test

echo "✅ Claude Code setup complete!"
```

### Windows PowerShell:
```powershell
Write-Host "🚀 Setting up Claude Code..." -ForegroundColor Green

# Install via npm
npm install -g @anthropic/claude-code

# Get API key
$apiKey = Read-Host "Enter your Anthropic API key" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey)
$key = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Set environment variable
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', $key, 'User')

# Test connection
claude test

Write-Host "✅ Claude Code setup complete!" -ForegroundColor Green
```

---

## 📝 Notes for Your Partner

### When Sharing the API Key:
1. **Send securely** (use password manager, encrypted message, or secure file transfer)
2. **Include rate limits** information if applicable
3. **Specify allowed usage** (development only, specific projects, etc.)
4. **Set expiration** if temporary access

### Message Template:
```
Hi [Partner],

Here's the setup for Claude Code:

1. API Key: [SEND SECURELY - NOT IN PLAIN TEXT]
2. Model to use: claude-3-opus-20240229
3. Rate limit: 1000 requests/day
4. Valid until: [DATE]

Please follow the setup guide at: CLAUDE_CODE_SETUP_GUIDE.md
Don't commit the API key to git!

Let me know if you have any issues.
```

---

## ✅ Setup Checklist

- [ ] System requirements met
- [ ] Claude Code installed
- [ ] API key configured
- [ ] Environment variables set
- [ ] `.gitignore` updated
- [ ] Connection tested
- [ ] VS Code extension installed (optional)
- [ ] Team settings configured
- [ ] Documentation reviewed

---

## 🆘 Getting Help

### If you encounter issues:
1. Check this guide's troubleshooting section
2. Run `claude doctor` for diagnostics
3. Visit [Claude Code Issues](https://github.com/anthropics/claude-code/issues)
4. Contact Anthropic support
5. Ask your partner for assistance

---

*Last updated: December 2024*
*Claude Code Version: Latest*

**Remember**: Keep your API key secure and never share it publicly! 🔐