#!/usr/bin/env python3
"""
Lars Vilhuber Chatbot
An interactive chatbot that emulates Lars Vilhuber's expertise and communication style
Based on analysis of his GitHub repositories and public work
"""

import random
import re
from typing import List, Dict, Tuple

class LarsVilhuberChatbot:
    def __init__(self):
        self.name = "Lars Vilhuber"
        self.title = "Data Editor, American Economic Association | Cornell University"
        self.initialize_knowledge_base()
        self.initialize_response_patterns()
        
    def initialize_knowledge_base(self):
        """Initialize the knowledge base with Lars's expertise areas"""
        self.expertise_areas = {
            "reproducibility": {
                "keywords": ["reproducible", "replication", "reproduce", "replicate", "computational"],
                "key_concepts": [
                    "computational empathy",
                    "hands-off running",
                    "trusted repositories",
                    "replication packages"
                ],
                "responses": [
                    "The key to reproducibility is what I call 'computational empathy' - thinking about what an unknown person attempting to reproduce your results might face.",
                    "A good replication package should run hands-off, without requiring manual intervention.",
                    "Remember, just because code runs on your computer doesn't mean it will run on someone else's.",
                    "I always recommend starting simple - can you run your code from start to finish without touching anything?"
                ]
            },
            "data_transparency": {
                "keywords": ["data", "transparency", "open", "access", "sharing"],
                "key_concepts": [
                    "data availability",
                    "data citations",
                    "trusted repositories",
                    "preservation"
                ],
                "responses": [
                    "Data transparency doesn't mean everything must be public - it means being clear about what exists and how to access it.",
                    "Even when data is confidential, we can be transparent about its provenance and characteristics.",
                    "Always cite your data sources properly - data creators deserve credit for their work.",
                    "Preservation is key - use trusted repositories like Zenodo, openICPSR, or Dataverse."
                ]
            },
            "software_environments": {
                "keywords": ["stata", "r", "python", "matlab", "julia", "software", "environment", "docker", "container"],
                "key_concepts": [
                    "environment management",
                    "version control",
                    "containerization",
                    "cross-platform compatibility"
                ],
                "responses": [
                    "Different researchers use different software - your package should be clear about requirements.",
                    "Consider using containers like Docker for complex environments - they ensure consistency.",
                    "Document your software versions explicitly - 'latest' is not a version number!",
                    "If using Stata, remember that not everyone has access to all packages or the latest version."
                ]
            },
            "best_practices": {
                "keywords": ["best", "practice", "recommend", "should", "how to", "guide"],
                "key_concepts": [
                    "documentation",
                    "README files",
                    "code organization",
                    "testing"
                ],
                "responses": [
                    "Start with a clear README - it's the first thing replicators will read.",
                    "Organize your code logically - separate data preparation from analysis.",
                    "Test your code on a clean machine or have a student run it - fresh eyes catch issues.",
                    "Document not just what your code does, but why you made certain choices."
                ]
            },
            "confidential_data": {
                "keywords": ["confidential", "restricted", "private", "sensitive", "access"],
                "key_concepts": [
                    "synthetic data",
                    "disclosure avoidance",
                    "access procedures",
                    "data enclaves"
                ],
                "responses": [
                    "When data is confidential, provide clear instructions on how others can gain access.",
                    "Consider creating synthetic data or a subset that demonstrates your code works.",
                    "Document the exact data structure even if you can't share the data itself.",
                    "Be transparent about what can and cannot be replicated with public data."
                ]
            }
        }
        
        self.teaching_phrases = [
            "Let me explain this step by step...",
            "The key thing to understand is...",
            "In my experience working with researchers...",
            "This is a common challenge, and here's how I approach it...",
            "Think about it from the replicator's perspective..."
        ]
        
        self.acknowledgment_phrases = [
            "That's a great question.",
            "This is something many researchers struggle with.",
            "You're right to be thinking about this.",
            "This is indeed important to consider.",
            "Good point - let me elaborate."
        ]
        
    def initialize_response_patterns(self):
        """Initialize conversational patterns based on Lars's style"""
        self.greeting_responses = [
            "Hello! I'm Lars Vilhuber, Data Editor at the American Economic Association. How can I help you with reproducibility today?",
            "Hi there! I work on data transparency and reproducibility in economics. What questions do you have?",
            "Welcome! I'm here to help with questions about replication packages, data citation, or reproducible research."
        ]
        
        self.clarification_requests = [
            "Could you tell me more about your specific situation?",
            "What software or data are you working with?",
            "Are you preparing a replication package or trying to reproduce someone else's work?",
            "What field of economics are you working in? Different fields have different conventions."
        ]
        
        self.closing_remarks = [
            "Remember, perfect is the enemy of good - start with making your work reproducible by yourself!",
            "Feel free to check out my self-checking reproducibility guide for more tips.",
            "Good luck with your research! The reproducibility community is here to help.",
            "Keep working on computational empathy - it gets easier with practice!"
        ]
        
    def find_topic(self, message: str) -> Tuple[str, float]:
        """Identify the main topic of the user's message"""
        message_lower = message.lower()
        best_match = None
        best_score = 0
        
        for topic, info in self.expertise_areas.items():
            score = sum(1 for keyword in info["keywords"] if keyword in message_lower)
            if score > best_score:
                best_score = score
                best_match = topic
                
        confidence = best_score / max(len(message_lower.split()), 1)
        return best_match, confidence
        
    def generate_response(self, message: str) -> str:
        """Generate a response based on the user's message"""
        message_lower = message.lower()
        
        # Handle greetings
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.greeting_responses)
            
        # Handle thanks/goodbye
        if any(word in message_lower for word in ["thank", "thanks", "bye", "goodbye"]):
            return random.choice(self.closing_remarks)
            
        # Find the main topic
        topic, confidence = self.find_topic(message)
        
        # If we're not confident about the topic, ask for clarification
        if confidence < 0.1 or topic is None:
            return random.choice(self.clarification_requests)
            
        # Build a response
        response_parts = []
        
        # Add acknowledgment
        if random.random() > 0.5:
            response_parts.append(random.choice(self.acknowledgment_phrases))
            
        # Add teaching phrase if appropriate
        if "how" in message_lower or "what" in message_lower or "why" in message_lower:
            response_parts.append(random.choice(self.teaching_phrases))
            
        # Add main response
        topic_info = self.expertise_areas[topic]
        main_response = random.choice(topic_info["responses"])
        response_parts.append(main_response)
        
        # Add specific advice based on keywords
        if "stata" in message_lower:
            response_parts.append("For Stata specifically, make sure to document which version you're using and list all required packages.")
        elif "python" in message_lower or "r" in message_lower:
            response_parts.append(f"For {('Python' if 'python' in message_lower else 'R')}, consider using virtual environments or renv to manage dependencies.")
        elif "student" in message_lower or "teach" in message_lower:
            response_parts.append("Teaching reproducibility is crucial - I recommend starting with simple examples and building up complexity.")
            
        return " ".join(response_parts)
        
    def chat(self):
        """Run an interactive chat session"""
        print("\n" + "="*60)
        print("Lars Vilhuber Chatbot")
        print("Based on analysis of public repositories and work")
        print("Type 'quit' or 'exit' to end the conversation")
        print("="*60 + "\n")
        
        print(random.choice(self.greeting_responses))
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print(f"\nLars: {random.choice(self.closing_remarks)}")
                    break
                    
                if not user_input:
                    continue
                    
                response = self.generate_response(user_input)
                print(f"\nLars: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\nLars: {random.choice(self.closing_remarks)}")
                break
            except Exception as e:
                print(f"\nLars: I apologize, but I encountered an issue. Could you rephrase your question?")
                continue

def main():
    """Main function to run the chatbot"""
    chatbot = LarsVilhuberChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()