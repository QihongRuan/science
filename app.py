#!/usr/bin/env python3
"""
Flask Web Application for Lars Vilhuber Chatbot
Provides a REST API and web interface for the chatbot
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import random
import re
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'lars-vilhuber-chatbot-secret-key-2024')
CORS(app)

# Store conversation histories (in production, use a database)
conversations = {}

class LarsVilhuberBot:
    """Core chatbot logic"""
    
    def __init__(self):
        self.initialize_knowledge_base()
        
    def initialize_knowledge_base(self):
        """Initialize comprehensive knowledge base"""
        
        self.expertise = {
            "computational_empathy": {
                "keywords": ["computational empathy", "empathy", "thinking about"],
                "responses": [
                    "Computational empathy is a concept I developed to describe thinking about what an unknown person attempting to reproduce your results might face. It means considering different operating systems, software versions, skill levels, and access to resources.",
                    "The key to computational empathy is documenting everything explicitly and testing your code as if you were a stranger to your own work. Ask yourself: would someone with a different setup be able to run this?"
                ]
            },
            "reproducibility": {
                "keywords": ["reproducible", "reproducibility", "replication", "replicate", "reproduce"],
                "responses": [
                    "Making research reproducible starts with good habits: clear file organization, documented dependencies, and tested code. I recommend the 'run it again' test - delete your output and see if you can recreate everything from scratch.",
                    "A good replication package has three key elements: all the data (or clear access instructions), all the code in runnable form, and clear documentation linking the code to the paper results.",
                    "Think of reproducibility as a ladder - each rung makes your work more accessible. Start with making it work for you, then a colleague, then someone in your field, then anyone."
                ]
            },
            "data_transparency": {
                "keywords": ["data", "transparency", "sharing", "access", "confidential", "restricted", "private"],
                "responses": [
                    "Data transparency doesn't mean everything must be public. When data can't be shared, document the data structure, provide access instructions, and consider creating synthetic data that demonstrates your code works.",
                    "Even with confidential data, we can be transparent about its provenance and characteristics. Document exactly what data you used, where it came from, and how others can access it if possible.",
                    "Data availability statements should be precise: what data exists, where it can be found, and what restrictions apply. 'Data available upon request' is no longer sufficient - be specific about the process."
                ]
            },
            "stata": {
                "keywords": ["stata"],
                "responses": [
                    "For Stata reproducibility: Always set the version explicitly with the 'version' command, document all ado files needed, and remember that not everyone has access to Stata/MP or the latest version.",
                    "In Stata, use 'ssc install' or 'net install' with specific sources for packages. Consider using 'creturn list' to document your system configuration. And always specify the exact Stata version you're using."
                ]
            },
            "r_language": {
                "keywords": ["\\br\\b", "rstudio", "r programming", "r language"],
                "responses": [
                    "For R reproducibility: Use renv for package management, document your R version and all package versions. Use sessionInfo() to capture your environment.",
                    "In R, consider using the groundhog package for date-based package versions. Be careful with compiled packages that may be OS-specific. Always include both your R version and package versions."
                ]
            },
            "python": {
                "keywords": ["python"],
                "responses": [
                    "For Python reproducibility: Use virtual environments or conda, create requirements.txt with specific versions using 'pip freeze'. Consider using poetry or pipenv for dependency management.",
                    "With Python, be explicit about the Python version (3.8, 3.9, etc.). Different versions can have subtle differences that affect results. Always include a requirements.txt with exact versions."
                ]
            },
            "docker": {
                "keywords": ["docker", "container", "singularity"],
                "responses": [
                    "Docker and containers provide complete environment reproducibility. They're especially useful for complex setups with multiple software dependencies. Start with a minimal base image and document the build process.",
                    "Containers like Docker ensure your code runs the same everywhere. While there's a learning curve, they solve many reproducibility issues. Consider them for projects with complex dependencies."
                ]
            },
            "readme": {
                "keywords": ["readme", "documentation", "document", "instructions"],
                "responses": [
                    "A good README should include: software requirements with versions, data availability statement, instructions to run the code, expected runtime, hardware requirements if substantial, and description of expected output.",
                    "Think of your README as a letter to a stranger who needs to understand and run your work. Be explicit about prerequisites, provide step-by-step instructions, and explain what they should expect to see."
                ]
            },
            "repositories": {
                "keywords": ["repository", "zenodo", "archive", "openicpsr", "dataverse", "preserve", "github"],
                "responses": [
                    "For long-term preservation, use trusted repositories. Zenodo is excellent and provides DOIs. OpenICPSR is the AEA's preferred repository. Harvard Dataverse is widely used in social sciences.",
                    "GitHub is great for collaboration but isn't an archive - it's for development, not preservation. For published work, use repositories that guarantee long-term preservation and provide DOIs."
                ]
            },
            "teaching": {
                "keywords": ["teach", "student", "education", "learning", "course", "class"],
                "responses": [
                    "Teaching reproducibility is crucial for the next generation. Start with simple exercises - have students reproduce a basic analysis, then gradually introduce complications.",
                    "The 'have an undergrad run it' test is remarkably effective for finding issues in your replication package! Fresh eyes catch problems you've become blind to."
                ]
            },
            "errors": {
                "keywords": ["error", "problem", "issue", "fail", "doesn't work", "broken"],
                "responses": [
                    "When encountering errors, first check: Are all required packages/software installed? Are you using the correct versions? Are file paths correct? These solve 90% of reproducibility issues.",
                    "Common reproducibility failures: hard-coded paths, missing dependencies, version mismatches, and platform-specific code. Document these potential issues in your README."
                ]
            },
            "best_practices": {
                "keywords": ["best practice", "recommend", "suggestion", "advice", "tips", "should i"],
                "responses": [
                    "My top recommendations: Start simple and build up. Test on a clean machine. Have someone else run your code. Document more than you think necessary. Use relative paths, not absolute ones.",
                    "Best practices: Organize files logically, use descriptive names, set random seeds, avoid manual steps, test everything, and remember - perfect is the enemy of good. Any documentation beats none."
                ]
            }
        }
        
        self.personality_phrases = {
            "greeting": [
                "Hello! I'm Lars Vilhuber, Data Editor at the American Economic Association. How can I help you with reproducibility today?",
                "Hi there! I work on data transparency and reproducibility in economics. What questions do you have?",
                "Welcome! I'm here to help with questions about replication packages, data citation, or reproducible research."
            ],
            "acknowledgment": [
                "That's a great question.",
                "This is something many researchers struggle with.",
                "You're right to be thinking about this.",
                "Good point - let me elaborate.",
                "This is indeed important to consider."
            ],
            "teaching": [
                "Let me break this down step by step.",
                "Here's how I think about this:",
                "In my experience with thousands of replication packages,",
                "The key insight here is",
                "Think about it this way:"
            ],
            "encouragement": [
                "You're on the right track!",
                "Every step toward reproducibility matters.",
                "Don't let perfect be the enemy of good.",
                "This is great progress!",
                "Keep up the good work!"
            ],
            "closing": [
                "Remember, perfect is the enemy of good - start with making your work reproducible by yourself!",
                "Feel free to check out my self-checking reproducibility guide for more tips.",
                "Good luck with your research! The reproducibility community is here to help.",
                "Keep working on computational empathy - it gets easier with practice!"
            ]
        }
        
    def find_best_response(self, message: str) -> Tuple[str, float]:
        """Find the best matching response for a message"""
        message_lower = message.lower()
        best_topic = None
        best_score = 0
        
        # Check each expertise area
        for topic, data in self.expertise.items():
            score = 0
            for keyword in data["keywords"]:
                if keyword in message_lower:
                    # Weight multi-word keywords higher
                    score += len(keyword.split())
            
            if score > best_score:
                best_score = score
                best_topic = topic
        
        confidence = best_score / max(len(message_lower.split()), 1)
        return best_topic, confidence
    
    def generate_response(self, message: str, conversation_history: List[Dict] = None) -> str:
        """Generate a contextual response"""
        message_lower = message.lower()
        
        # Handle greetings
        if any(g in message_lower for g in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.personality_phrases["greeting"])
        
        # Handle thanks/goodbye
        if any(word in message_lower for word in ["thank", "thanks", "bye", "goodbye"]):
            return random.choice(self.personality_phrases["closing"])
        
        # Find best matching topic
        topic, confidence = self.find_best_response(message)
        
        # Build response
        response_parts = []
        
        # Add acknowledgment for good questions
        if confidence > 0.2 and random.random() > 0.5:
            response_parts.append(random.choice(self.personality_phrases["acknowledgment"]))
        
        # Add teaching phrase for complex topics
        if "how" in message_lower or "what" in message_lower or "why" in message_lower:
            if random.random() > 0.6:
                response_parts.append(random.choice(self.personality_phrases["teaching"]))
        
        # Add main response
        if topic and confidence > 0.1:
            response_parts.append(random.choice(self.expertise[topic]["responses"]))
        else:
            # Default responses for unclear questions
            defaults = [
                "Could you tell me more about your specific situation? Are you working with a particular software or type of data?",
                "I'd be happy to help! Could you provide more details about what aspect of reproducibility you're interested in?",
                "That's interesting. To give you the most relevant advice, could you tell me what software you're using and what kind of project you're working on?",
                "Let me understand better - are you preparing a replication package, or trying to reproduce someone else's work?"
            ]
            response_parts.append(random.choice(defaults))
        
        # Add encouragement occasionally
        if random.random() > 0.8:
            response_parts.append(random.choice(self.personality_phrases["encouragement"]))
        
        return " ".join(response_parts)

# Initialize the bot
bot = LarsVilhuberBot()

@app.route('/')
def index():
    """Serve the main chat interface"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        conversations[session['session_id']] = []
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages via API"""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to history
    conversations[session_id].append({
        'role': 'user',
        'content': message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Generate response
    response = bot.generate_response(message, conversations[session_id])
    
    # Add bot response to history
    conversations[session_id].append({
        'role': 'assistant',
        'content': response,
        'timestamp': datetime.now().isoformat()
    })
    
    # Limit conversation history to last 50 messages
    if len(conversations[session_id]) > 50:
        conversations[session_id] = conversations[session_id][-50:]
    
    return jsonify({
        'response': response,
        'session_id': session_id
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation history"""
    data = request.json
    session_id = data.get('session_id')
    
    if session_id in conversations:
        conversations[session_id] = []
    
    return jsonify({'status': 'success', 'message': 'Conversation reset'})

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'bot': 'Lars Vilhuber Chatbot'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)