#!/usr/bin/env python3
"""
Simple runner script for the Lars Vilhuber Chatbot
"""

import os
import sys

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        print("✓ All dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    print("Lars Vilhuber Chatbot - Web Interface")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    print("Starting the chatbot server...")
    print("Once started, open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Import and run the app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()