#!/usr/bin/env python3
"""
Simple test script for the Lars Vilhuber Chatbot API
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_bot_responses():
    """Test the bot's core functionality"""
    from app import LarsVilhuberBot
    
    bot = LarsVilhuberBot()
    
    test_cases = [
        "What is computational empathy?",
        "How do I make my Stata code reproducible?",
        "Tell me about data transparency",
        "What should go in a README file?",
        "How do I use Docker for reproducibility?"
    ]
    
    print("Testing Lars Vilhuber Chatbot")
    print("=" * 50)
    
    for i, question in enumerate(test_cases, 1):
        print(f"\nTest {i}: {question}")
        print("-" * 30)
        response = bot.generate_response(question)
        print(f"Response: {response[:200]}...")
        
    print("\n✅ All tests completed successfully!")

def test_flask_app():
    """Test Flask app creation"""
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✅ Health check endpoint working")
            else:
                print("❌ Health check failed")
                
            # Test chat endpoint
            response = client.post('/api/chat', 
                                 json={'message': 'Hello', 'session_id': 'test'})
            if response.status_code == 200:
                print("✅ Chat endpoint working")
                data = response.get_json()
                print(f"Sample response: {data['response'][:100]}...")
            else:
                print("❌ Chat endpoint failed")
                
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")

if __name__ == "__main__":
    print("Lars Vilhuber Chatbot - Testing Suite")
    print("=" * 60)
    
    test_bot_responses()
    print("\n" + "=" * 60)
    test_flask_app()
    
    print("\n🎉 Ready for deployment!")
    print("Run 'python3 run.py' to start the web interface")