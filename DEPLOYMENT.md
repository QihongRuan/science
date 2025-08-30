# Lars Vilhuber Chatbot - Deployment Guide

This guide explains how to deploy the Lars Vilhuber Chatbot web application for general users.

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### 2. Installation
```bash
# Clone or download the project
cd lars

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### 3. Access
Open your web browser and go to: `http://localhost:5000`

## Production Deployment Options

### Option 1: Using Gunicorn (Recommended)

1. **Install Gunicorn:**
```bash
pip install gunicorn
```

2. **Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **With environment variables:**
```bash
export SECRET_KEY="your-secret-key-here"
export PORT=5000
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### Option 2: Docker Deployment

1. **Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

2. **Build and run:**
```bash
docker build -t lars-chatbot .
docker run -p 5000:5000 lars-chatbot
```

### Option 3: Heroku Deployment

1. **Create Procfile:**
```
web: gunicorn app:app
```

2. **Deploy to Heroku:**
```bash
heroku create your-app-name
git push heroku main
```

### Option 4: Railway Deployment

1. **Connect your GitHub repository to Railway**
2. **Railway will automatically detect the Flask app**
3. **Set environment variables if needed**

### Option 5: Render Deployment

1. **Create a new Web Service on Render**
2. **Connect your GitHub repository**
3. **Use these settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

## Environment Variables

You can customize the application with these environment variables:

- `SECRET_KEY`: Flask secret key for sessions (default: auto-generated)
- `PORT`: Port to run on (default: 5000)
- `FLASK_ENV`: Set to `production` for production deployment

## Nginx Configuration (Optional)

For production with Nginx reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Performance Considerations

### For High Traffic:

1. **Use multiple workers:**
```bash
gunicorn -w 8 -b 0.0.0.0:5000 app:app
```

2. **Add Redis for session storage:**
```bash
pip install redis flask-session
```

Then modify `app.py` to use Redis for sessions.

3. **Use a proper database:**
Replace the in-memory conversation storage with PostgreSQL or MongoDB.

## Security Considerations

1. **Set a strong SECRET_KEY:**
```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

2. **Use HTTPS in production**

3. **Rate limiting:**
```bash
pip install flask-limiter
```

4. **CORS configuration:**
Update CORS settings in `app.py` for your specific domain.

## Monitoring and Logging

### Basic logging setup:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### For production, consider:
- Application Performance Monitoring (APM) tools
- Log aggregation services
- Health check endpoints (already included at `/api/health`)

## Scaling Options

### Horizontal Scaling:
- Deploy multiple instances behind a load balancer
- Use container orchestration (Kubernetes, Docker Swarm)
- Cloud services with auto-scaling

### Database Scaling:
- Replace in-memory storage with persistent database
- Use connection pooling
- Consider read replicas for high read loads

## Troubleshooting

### Common Issues:

1. **Port already in use:**
```bash
# Find what's using the port
lsof -i :5000
# Kill the process or use a different port
```

2. **Dependencies not found:**
```bash
pip install -r requirements.txt
```

3. **Permission denied:**
```bash
# On Linux/Mac, you might need to use a port > 1024 for non-root users
python run.py  # Uses port 5000 by default
```

### Health Check:
Visit `http://your-domain/api/health` to verify the service is running.

## API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send chat messages
- `POST /api/reset` - Reset conversation
- `GET /api/health` - Health check

## Customization

### Adding new expertise areas:
Edit the `expertise` dictionary in `app.py` to add new topics.

### Changing the personality:
Modify the `personality_phrases` in `app.py`.

### Updating the UI:
Edit `templates/chat.html` for interface changes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the application logs
3. Test the API endpoints directly

The chatbot is designed to be lightweight and easy to deploy on various platforms.