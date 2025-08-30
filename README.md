# Lars Vilhuber Chatbot Collection

An interactive chatbot system that emulates the expertise and communication style of Lars Vilhuber, Data Editor at the American Economic Association and expert in reproducibility and data transparency in economics.

## About Lars Vilhuber

Lars Vilhuber is:
- Data Editor, American Economic Association (AEA)
- Executive Director, Labor Dynamics Institute at Cornell University
- Senior Research Associate, Cornell University Economics Department
- Leading expert in computational reproducibility and data transparency

His work focuses on:
- Making economics research more reproducible
- Data transparency and access procedures
- Teaching best practices for replication packages
- "Computational empathy" - considering what replicators face

## Chatbot Implementations

### 1. Basic Python Chatbot (`lars_vilhuber_chatbot.py`)

A simple command-line chatbot with core knowledge areas:
- Reproducibility practices
- Data transparency
- Software environments
- Best practices
- Confidential data handling

**Usage:**
```bash
python lars_vilhuber_chatbot.py
```

### 2. Advanced Python Chatbot (`lars_chatbot_advanced.py`)

An enhanced version with:
- Contextual awareness and conversation memory
- User experience level detection
- Software-specific guidance
- Comprehensive knowledge base
- Personality traits based on communication style analysis

**Usage:**
```bash
python lars_chatbot_advanced.py
```

**Commands:**
- Type `help` - Get list of topics
- Type `reset` - Clear conversation context
- Type `quit` or `exit` - End conversation

### 3. Web Interface (`chatbot_web.html`)

A simple browser-based chat interface with no server required:
- Modern, responsive design
- Quick action buttons for common questions
- No external dependencies

**Usage:**
Simply open `chatbot_web.html` in any modern web browser.

### 4. **Web Application with Flask Backend (Recommended for general users)**

A complete web application with:
- Modern, responsive web interface
- Real-time chat with backend API
- Session management
- Quick topic buttons
- Professional UI/UX design
- Easy deployment options

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python3 run.py
```

Then open `http://localhost:5000` in your browser.

**Features:**
- Professional chat interface with avatars
- Typing indicators and smooth animations
- Session persistence
- Reset conversation functionality
- Mobile-responsive design
- RESTful API endpoints

### 5. Optional: Fine-tuned GPT backend

You can optionally fine-tune a GPT model on this project's curated knowledge and have the Flask app call that model. See section "Fine-tuning and integration" below.

## Key Features

### Knowledge Areas Covered

1. **Computational Empathy**
   - Understanding replicator perspectives
   - Cross-platform considerations
   - Skill level variations

2. **Reproducibility**
   - Step-by-step guidance
   - Testing methods
   - Package organization

3. **Data Transparency**
   - Handling confidential data
   - Data availability statements
   - Access procedures

4. **Software Environments**
   - Stata, R, Python, MATLAB, Julia
   - Version management
   - Container solutions

5. **Documentation Standards**
   - README essentials
   - Folder organization
   - Code documentation

6. **Repository Selection**
   - Zenodo, OpenICPSR, Dataverse
   - Long-term preservation
   - DOI assignment

## Installation

### Python Chatbots

No special installation required for basic functionality. Python 3.6+ recommended.

```bash
# Clone or download the files
# Run directly with Python
python lars_vilhuber_chatbot.py
# or
python lars_chatbot_advanced.py
```

### Web Interface

No installation needed - just open the HTML file in a browser:
- Chrome, Firefox, Safari, Edge all supported
- No internet connection required
- No server setup needed

## Chatbot Personality

Based on analysis of Lars Vilhuber's public repositories and work, the chatbot emulates:

### Communication Style
- Clear, educational explanations
- Patient and encouraging tone
- Practical, solution-focused advice
- Recognition of real-world constraints

### Core Principles
- "Perfect is the enemy of good"
- Start simple and build up
- Focus on computational empathy
- Transparency over perfection

### Teaching Approach
- Step-by-step guidance
- Multiple examples
- Acknowledgment of challenges
- Encouragement for incremental progress

## Example Interactions

### Basic Questions
- "What is computational empathy?"
- "How do I make my research reproducible?"
- "What should go in a README file?"

### Software-Specific
- "How do I handle Stata package dependencies?"
- "What's the best way to manage R environments?"
- "Should I use Docker for my project?"

### Data Issues
- "My data is confidential - how can I be transparent?"
- "Where should I archive my replication package?"
- "How do I write a data availability statement?"

## Limitations

These chatbots are educational demonstrations based on public information. They:
- Don't have access to real-time information
- Can't make official AEA policy statements
- Provide general guidance, not specific reviews
- Are not connected to actual Lars Vilhuber

## Resources

For official resources, see:
- [Self-Checking Reproducibility Guide](https://larsvilhuber.github.io/self-checking-reproducibility/)
- [AEA Data Editor](https://aeadataeditor.github.io/)
- [Social Science Data Editors](https://social-science-data-editors.github.io/)

## Additional Guides

- [Atlassian vs GitHub: Selection Guide](./ATLASSIAN_GITHUB_GUIDE.md)

## License

MIT

---
*Created: 2025-08-30*

---

## Fine-tuning and integration

1) Prepare dataset

```bash
python3 tools/build_finetune_dataset.py --out data/finetune.jsonl
```

2) Start fine-tuning (requires OpenAI API key)

```bash
export OPENAI_API_KEY=...  # your key
python3 tools/start_finetune.py data/finetune.jsonl
```

This prints a fine-tuned model id (e.g., ft:gpt-4o-mini:org:slug:xxxx). Save it to `.env` as `FINE_TUNED_MODEL=...`.

3) Run server using the fine-tuned model

```bash
export USE_OPENAI=1
export FINE_TUNED_MODEL=ft:your-model-id
python3 run.py
```

When `USE_OPENAI=1` is set, the app will call the fine-tuned model; otherwise it uses the built-in rules-based bot.