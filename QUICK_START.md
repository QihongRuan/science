# Quick Start Guide - Lars Vilhuber Chatbot

The easiest way to get the Lars Vilhuber Chatbot running for general users.

## 🚀 For General Users (Recommended)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Application
```bash
python3 run.py
```

### 3. Open in Browser
Go to: **http://localhost:5000**

That's it! You now have a professional chat interface to talk with the Lars Vilhuber chatbot about reproducibility and data transparency.

## 🎯 What You Can Ask

### Quick Topics (click buttons in the interface):
- **Computational Empathy** - Lars's signature concept
- **Reproducibility Basics** - Getting started with reproducible research
- **Confidential Data** - Handling sensitive data transparently
- **README Template** - What to include in documentation
- **Stata Best Practices** - Stata-specific reproducibility tips
- **Docker & Containers** - Using containers for reproducibility
- **Data Repositories** - Where to archive your research

### Example Questions:
- "What is computational empathy?"
- "How do I make my Stata code reproducible?"
- "My data is confidential - how can I be transparent?"
- "What should go in a README file?"
- "Should I use Docker for my project?"
- "Where should I archive my replication package?"
- "How do I handle R package dependencies?"

## 🌐 Deployment for Others

### Share Locally (Same Network)
```bash
# Run on all interfaces
python3 run.py
# Then share: http://YOUR-IP-ADDRESS:5000
```

### Deploy Online
See `DEPLOYMENT.md` for full deployment options including:
- Heroku (free tier available)
- Railway (free tier available) 
- Render (free tier available)
- Docker deployment
- VPS deployment

## 🔧 Files Overview

- `app.py` - Main Flask web application
- `run.py` - Simple runner script
- `templates/chat.html` - Web interface
- `requirements.txt` - Python dependencies
- `test_app.py` - Test the installation

## 💡 Key Features

✅ **Professional chat interface** - Clean, modern design  
✅ **Real-time responses** - Instant chat experience  
✅ **Session management** - Conversations are remembered  
✅ **Mobile responsive** - Works on phones and tablets  
✅ **Quick topics** - One-click common questions  
✅ **Easy deployment** - Multiple hosting options  
✅ **No database required** - Simple setup  

## 🆘 Need Help?

1. **Installation issues?** Check you have Python 3.7+ installed
2. **Port conflicts?** Edit `run.py` to use a different port
3. **Dependencies?** Run `pip install -r requirements.txt` again
4. **Test the setup:** Run `python3 test_app.py`

## 🎓 About Lars Vilhuber

This chatbot is based on the expertise of Lars Vilhuber:
- Data Editor, American Economic Association
- Executive Director, Labor Dynamics Institute, Cornell University
- Leading expert in computational reproducibility
- Creator of the "computational empathy" concept

The chatbot provides his guidance on making economics research more reproducible and transparent, based on analysis of his extensive public work and repositories.

---

**Ready to chat about reproducibility? Run `python3 run.py` and visit http://localhost:5000**