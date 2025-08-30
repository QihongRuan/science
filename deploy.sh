#!/bin/bash

# Deploy Lars Vilhuber Chatbot to various platforms
# Run: ./deploy.sh [platform]

set -e

echo "🤖 Lars Vilhuber Chatbot Deployment Script"
echo "==========================================="

PLATFORM=${1:-"help"}

case $PLATFORM in
  "render")
    echo "📡 Deploying to Render..."
    echo ""
    echo "1. Go to https://render.com and create an account"
    echo "2. Connect your GitHub repository"
    echo "3. Create a new Web Service"
    echo "4. Use these settings:"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: gunicorn app:app"
    echo "   - Environment: Python 3"
    echo ""
    echo "Your chatbot will be live at: https://your-service-name.onrender.com"
    ;;
    
  "railway")
    echo "🚂 Deploying to Railway..."
    echo ""
    echo "1. Go to https://railway.app and create an account"
    echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
    echo "3. Select your repository"
    echo "4. Railway will auto-detect the Flask app"
    echo ""
    echo "Your chatbot will be live at: https://your-app.up.railway.app"
    ;;
    
  "heroku")
    echo "🟣 Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Install from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Create Procfile for Heroku
    echo "web: gunicorn app:app" > Procfile
    echo "✅ Created Procfile"
    
    # Check if git repo exists
    if [ ! -d ".git" ]; then
        echo "Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit for Lars Vilhuber Chatbot"
    fi
    
    # Create Heroku app
    echo "Creating Heroku app..."
    APP_NAME="lars-vilhuber-chatbot-$(date +%s)"
    heroku create $APP_NAME
    
    # Deploy
    echo "Deploying to Heroku..."
    git push heroku main
    
    echo ""
    echo "🎉 Deployment complete!"
    echo "Your chatbot is live at: https://$APP_NAME.herokuapp.com"
    ;;
    
  "docker")
    echo "🐳 Creating Docker setup..."
    
    # Create Dockerfile
    cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
EOF
    
    # Create docker-compose.yml
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  lars-chatbot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
EOF
    
    echo "✅ Created Dockerfile and docker-compose.yml"
    echo ""
    echo "To run with Docker:"
    echo "  docker build -t lars-chatbot ."
    echo "  docker run -p 5000:5000 lars-chatbot"
    echo ""
    echo "Or with docker-compose:"
    echo "  docker-compose up"
    ;;
    
  "github-pages")
    echo "📄 Setting up GitHub Pages (Static Version)..."
    
    # Create a simple index.html that redirects to the static version
    cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Lars Vilhuber Chatbot</title>
    <script>
        window.location.href = 'chatbot_web.html';
    </script>
</head>
<body>
    <p>Redirecting to <a href="chatbot_web.html">Lars Vilhuber Chatbot</a>...</p>
</body>
</html>
EOF
    
    echo "✅ Created index.html for GitHub Pages"
    echo ""
    echo "To deploy:"
    echo "1. Push this repository to GitHub"
    echo "2. Go to repository Settings → Pages"
    echo "3. Select 'Deploy from branch' → 'main'"
    echo ""
    echo "Your chatbot will be live at:"
    echo "https://yourusername.github.io/your-repo-name/"
    ;;
    
  "test")
    echo "🧪 Testing the application..."
    python3 test_app.py
    ;;
    
  "help"|*)
    echo "Usage: ./deploy.sh [platform]"
    echo ""
    echo "Available platforms:"
    echo "  render        - Deploy to Render (recommended)"
    echo "  railway       - Deploy to Railway"  
    echo "  heroku        - Deploy to Heroku (requires Heroku CLI)"
    echo "  docker        - Create Docker setup files"
    echo "  github-pages  - Setup for GitHub Pages (static version)"
    echo "  test          - Test the application locally"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh render"
    echo "  ./deploy.sh test"
    echo ""
    echo "For detailed instructions, see:"
    echo "  - DEPLOYMENT.md (full deployment guide)"
    echo "  - USER_INSTRUCTIONS.md (how users access it)"
    ;;
esac

echo ""
echo "📚 For more help, see:"
echo "  - DEPLOYMENT.md - Full deployment guide"
echo "  - USER_INSTRUCTIONS.md - How users can access the chatbot"
echo "  - QUICK_START.md - Local installation guide"