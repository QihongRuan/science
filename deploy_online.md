# Deploy Lars Vilhuber Chatbot Online

## Free Hosting Options for Users to Access Without Installing

### Option A: Render (Recommended - Very Easy)

1. **Create account at render.com**
2. **Connect your GitHub repository**
3. **Create new Web Service with these settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Auto-deploy: Yes

**Result:** Users get a URL like `https://lars-chatbot.onrender.com` - no installation needed!

### Option B: Railway

1. **Go to railway.app and connect GitHub**
2. **Deploy from repository**
3. **Railway auto-detects Flask app**

**Result:** Users get a URL like `https://lars-chatbot-production.up.railway.app`

### Option C: Heroku

1. **Create Procfile:**
```
web: gunicorn app:app
```

2. **Deploy to Heroku:**
```bash
heroku create lars-vilhuber-chatbot
git push heroku main
```

**Result:** Users get `https://lars-vilhuber-chatbot.herokuapp.com`

## For the Repository Owner

### Step 1: Choose a hosting service (I recommend Render)
### Step 2: Connect your GitHub repository
### Step 3: Deploy with one click
### Step 4: Share the URL with users

## What Users Experience

✅ **Just visit a website** - No installation required  
✅ **Works on any device** - Phone, tablet, computer  
✅ **No technical knowledge needed** - Just like any website  
✅ **Always up-to-date** - You control updates  

## Cost
- **Render:** Free tier available (some limitations)
- **Railway:** Free tier available (some limitations) 
- **Heroku:** Free tier discontinued, paid plans available

## Example User Instructions (After Deployment)

> **"Chat with Lars Vilhuber about reproducibility!"**
> 
> Simply visit: **https://your-chatbot-url.com**
> 
> No installation required - works in any web browser.
> Ask about reproducibility, data transparency, Stata, R, Python, and more!

## Alternative: GitHub Pages (Static Version)

For a simpler approach, you could create a static version using GitHub Pages with the existing `chatbot_web.html` file (though less sophisticated than the Flask version).

1. Enable GitHub Pages in repository settings
2. Users visit: `https://yourusername.github.io/lars/chatbot_web.html`