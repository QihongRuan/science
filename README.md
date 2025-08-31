# Lars Research Repository

This repository contains multiple projects and research initiatives by Qihong Ruan, focusing on economic research, AI applications, and academic reproducibility.

## 🚀 Featured Project: SciAgent Lab (AI Agent 2025 Competition)

### 科研多智能体实验助手 (SciAgent Lab)
**AI Agent 2025 全球专项赛参赛项目**

A comprehensive AI agents platform designed for scientific research automation, featuring multi-agent collaboration for the complete research cycle: literature → hypothesis → experiment → data → conclusions.

**Quick Links:**
- 📄 [Business Plan (Chinese)](./docs/AI_Agent_2025_商业计划书_提交版.pdf)
- 📋 [Project Overview](./docs/README.md)
- 🖼️ [Project Cover Image](./SciAgents.png)
- 📊 [Project Index](./SCIAGENT_PROJECT.md)

**Key Features:**
- Multi-agent research workflow automation
- RAG + causal inference for literature analysis
- Automated hypothesis generation and experimental design
- Integration with LIMS/ELN and research tools
- 100% reproducible research reports

**Target Users:** Research labs, universities, R&D teams in pharma, materials, and chemical industries.

## 📊 AEA Research & Reproducibility Studies

### American Economic Association (AEA) Replication Analysis
Extensive analysis of economic research reproducibility based on AEA replication packages and standards.

**Key Components:**
- [AEA Writing Patterns Analysis](./AER_WRITING_PATTERNS.md)
- [Remarkable Research Findings](./AER_REMARKABLE_FINDINGS.md)
- [Fama-MacBeth Analysis Implementation](./FAMA_MACBETH_ANALYSIS.md)
- [Comprehensive Insights Report](./COMPREHENSIVE_INSIGHTS_REPORT.md)

**Research Scripts:**
- [`analyze_repos.py`](./analyze_repos.py) - Automated repository analysis
- [`econometric_analysis.py`](./econometric_analysis.py) - Economic method implementations
- [`scripts/auto_analyze_papers.sh`](./scripts/auto_analyze_papers.sh) - Batch paper analysis

## 🤖 Lars Vilhuber Chatbot Collection

An interactive chatbot system that emulates the expertise and communication style of Lars Vilhuber, Data Editor at the American Economic Association and expert in reproducibility and data transparency.

### Available Implementations

1. **Web Application with Flask Backend** (Recommended)
   ```bash
   pip install -r requirements.txt
   python3 run.py
   ```
   Open `http://localhost:5000` in your browser.

2. **Command Line Chatbots**
   ```bash
   python lars_vilhuber_chatbot.py        # Basic version
   python lars_chatbot_advanced.py        # Advanced with context
   ```

3. **Static Web Interface**
   Open `chatbot_web.html` in any modern browser.

### Knowledge Areas
- Computational reproducibility and empathy
- Data transparency and confidentiality
- Software environments (Stata, R, Python, MATLAB, Julia)
- Repository selection and data archiving
- Documentation standards and best practices

## 🛠️ Utility Scripts & Tools

### PDF Processing & Analysis
- [`scripts/create_clean_pdf.sh`](./scripts/create_clean_pdf.sh) - Generate clean PDFs without headers/footers
- [`scripts/html_to_pdf.sh`](./scripts/html_to_pdf.sh) - HTML to PDF conversion
- [`scripts/extract_pdf_writing_patterns.py`](./scripts/extract_pdf_writing_patterns.py) - Extract writing patterns from academic PDFs

### Documentation & Guides
- [Claude Code Setup Guide](./CLAUDE_CODE_SETUP_GUIDE.md) - Complete setup instructions for Claude Code
- [Atlassian vs GitHub Guide](./ATLASSIAN_GITHUB_GUIDE.md) - Platform selection guidance
- [Data Repositories Guide](./DATA_REPOSITORIES.md) - Research data management

## 📁 Repository Structure

```
├── docs/                          # SciAgent Lab project documentation
│   ├── README.md                  # Detailed project overview
│   ├── AI_Agent_2025_*.pdf        # Business plans and submissions
│   └── 项目*.md                   # Chinese project documentation
├── paper_analysis/                # Analyzed academic papers
├── pdf_text/                      # Extracted PDF text content
├── scripts/                       # Utility scripts and tools
├── templates/                     # Document templates
└── [chatbot files]               # Lars Vilhuber chatbot implementations
```

## 🎯 Research Focus Areas

1. **AI Agents for Scientific Research**
   - Multi-agent system design
   - Research workflow automation
   - Reproducibility and compliance

2. **Economic Research Analysis**
   - AEA replication standards
   - Econometric method implementation
   - Research pattern analysis

3. **Academic Reproducibility**
   - Computational empathy principles
   - Data transparency practices
   - Documentation standardization

## 🤝 Collaboration & Contact

**Qihong Ruan**
- Cornell University Economics PhD
- AEA Replication Project Contributor
- Specializing in causal inference and data governance

For SciAgent Lab collaboration:
- 📧 Business inquiries welcome
- 🤖 Seeking AI engineers and full-stack developers
- 🔬 Looking for scientific advisors in life sciences, materials, chemistry

## 📜 License

MIT License - See individual project folders for specific licensing information.

---

*This repository represents ongoing research in AI-assisted scientific discovery, economic analysis, and academic reproducibility. All projects emphasize transparency, reproducibility, and practical applications.*

**Last Updated:** 2025-08-31