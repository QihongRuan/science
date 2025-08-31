# Prompt for Setting Up Claude Code with API Key via Codex CLI

## Copy and paste this entire prompt to Codex:

---

I need help setting up Claude Code to use with my API key for academic research. Please guide me through the complete setup process.

**My Setup Requirements:**
1. I want to use Claude Code with my Anthropic API key (not login-based authentication)
2. I need this for analyzing economics research code and writing an academic paper
3. I want to use the most powerful model available (Claude 3 Opus)
4. My operating system is: [SPECIFY: macOS/Windows/Linux]
5. I have my API key ready: `sk-ant-api03-[YOUR-KEY-HERE]`

**Please help me:**

1. **Install Claude Code** using the best method for my system
2. **Configure the API key** properly and securely
3. **Set up the optimal configuration** for academic research and code analysis
4. **Test the setup** to ensure everything works
5. **Create a project-specific configuration** for my economics research paper

**Specific Configuration Needs:**

```json
{
  "model": "claude-3-opus-20240229",
  "maxTokens": 4096,
  "temperature": 0.7,
  "purpose": "Academic research - analyzing AEA replication packages",
  "requirements": [
    "Code analysis capabilities",
    "Long context for reading multiple files",
    "Ability to write academic prose",
    "Statistical code understanding (Stata, R, Python)"
  ]
}
```

**Project Context:**
I'm writing a paper analyzing 158 AEA (American Economic Association) replication packages to extract insights about computational practices in economics. I need Claude to:
- Analyze Stata, R, Python, and MATLAB code
- Identify best practices and anti-patterns
- Generate academic writing about findings
- Create statistical summaries
- Suggest improvements to reproducibility

**Security Requirements:**
- API key should not be in my command history
- Should not be committed to git
- Need to share setup with co-authors safely

**Expected Workflow:**
```bash
# I want to be able to do:
claude analyze path/to/repo --output analysis.md
claude "summarize the econometric methods in these files"
claude "write a paragraph about reproducibility issues found"
```

**Please provide:**
1. Step-by-step installation commands
2. Configuration file templates
3. Environment variable setup
4. Test commands to verify it works
5. Best practices for my use case
6. How to switch between models if needed
7. How to monitor API usage and costs

**Additional Questions:**
- Should I use a separate API key for this project?
- How do I set spending limits?
- Can I log all interactions for my research?
- Best way to handle large codebases (14GB of repos)?
- How to batch process multiple repositories?

**My System Info:**
```bash
# [Paste output of these commands]
echo $SHELL
python --version
node --version
echo $PATH
```

Please provide complete, copy-paste ready commands and explain any important decisions I need to make.

---

## Alternative Shorter Version (if you want something more concise):

---

Help me set up Claude Code with my Anthropic API key for academic research.

**Quick Setup Needed:**
- Install Claude Code on [YOUR OS]
- Configure with API key: `sk-ant-api03-[YOUR-KEY]`
- Optimize for analyzing economics code (Stata, R, Python)
- Set up for academic paper writing

**Commands I need:**
1. Installation
2. API key configuration  
3. Test that it works
4. Best settings for code analysis

I'm analyzing 158 economics research repositories for a paper on computational reproducibility.

Please provide copy-paste ready commands.

---

## After Setup, Test With:

```bash
# Test basic functionality
claude --version
claude test

# Test your use case
echo "Analyze this Stata code: reg y x, robust" | claude

# Test file analysis
claude "What does this code do?" --file sample.do

# Test longer analysis
claude "Write a paragraph about reproducibility best practices in economics"
```

## Important Notes to Include:

⚠️ **Before sharing with Codex, replace `[YOUR-KEY-HERE]` with your actual API key**

⚠️ **Mention if you need:**
- Team collaboration setup
- Specific spending limits
- Integration with existing tools
- Custom aliases or shortcuts

## For Your Paper Specifically:

After setup, you can use these commands for your paper:

```bash
# Analyze a single repository
claude "Analyze the code quality and reproducibility of this repository" --path ./AEAREP-103-ssh/repo-name/

# Batch analysis
for repo in ./AEAREP-103-ssh/*/; do
    claude "Rate reproducibility 1-10 with reasons" --path "$repo" >> analysis_results.txt
done

# Generate paper sections
claude "Write an academic paragraph about the computational practices found in these Stata files" --path ./stata_files/

# Statistical analysis
claude "Create a table summarizing the methods used across all repositories" --file methods_summary.json
```

## Cost Optimization Tips to Ask About:

1. How to use cheaper models for initial analysis (Claude Instant)
2. How to cache responses to avoid repeated API calls
3. How to estimate costs before running large batches
4. How to set up hard spending limits

---

**Final Note**: Save this configuration for your co-authors:

```bash
# Create shareable setup script
cat > setup_claude_for_paper.sh << 'EOF'
#!/bin/bash
echo "Setting up Claude Code for AEA Repository Analysis"
export ANTHROPIC_API_KEY="$1"  # Pass key as argument
claude config set model claude-3-opus-20240229
claude config set max-tokens 4096
echo "Setup complete. Test with: claude test"
EOF

# Share with co-authors (they run):
bash setup_claude_for_paper.sh their-api-key
```