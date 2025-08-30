#!/usr/bin/env python3
"""
Advanced Lars Vilhuber Chatbot with Enhanced Knowledge Base
Incorporates deep understanding of reproducibility, data transparency, and economics research
"""

import json
import random
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class ResearchContext:
    """Context for maintaining conversation state"""
    current_topic: Optional[str] = None
    software_mentioned: List[str] = field(default_factory=list)
    user_experience_level: str = "unknown"
    questions_asked: List[str] = field(default_factory=list)
    advice_given: List[str] = field(default_factory=list)

class LarsVilhuberAdvancedChatbot:
    def __init__(self):
        self.name = "Lars Vilhuber"
        self.roles = [
            "Data Editor, American Economic Association",
            "Executive Director, Labor Dynamics Institute",
            "Senior Research Associate, Cornell University"
        ]
        self.context = ResearchContext()
        self.initialize_comprehensive_knowledge()
        self.initialize_personality_traits()
        
    def initialize_comprehensive_knowledge(self):
        """Initialize comprehensive knowledge base from repository analysis"""
        
        self.core_principles = {
            "computational_empathy": {
                "definition": "Thinking about what an unknown person attempting to reproduce results might face",
                "applications": [
                    "Consider different operating systems",
                    "Account for varying software access",
                    "Think about different skill levels",
                    "Anticipate missing dependencies"
                ]
            },
            "transparency_spectrum": {
                "levels": [
                    "Full open access",
                    "Restricted access with clear procedures",
                    "Synthetic data with real structure",
                    "Detailed documentation without data"
                ],
                "principle": "Be as open as possible, as closed as necessary"
            },
            "reproducibility_hierarchy": {
                "levels": [
                    "Runs on my machine",
                    "Runs on a clean machine of same OS",
                    "Runs on different OS",
                    "Runs with different software versions",
                    "Runs by someone unfamiliar with the methods"
                ]
            }
        }
        
        self.software_expertise = {
            "stata": {
                "versions": "Consider version compatibility, especially for commands introduced in recent versions",
                "packages": "Use 'ssc install' or 'net install' with specific sources",
                "licensing": "Remember not everyone has access to Stata/MP or all packages",
                "tips": [
                    "Set version explicitly with 'version' command",
                    "Document all ado files needed",
                    "Consider using creturn list to document system"
                ]
            },
            "r": {
                "environment": "Use renv for package management",
                "versions": "Document R version and all package versions",
                "tips": [
                    "Use sessionInfo() to capture environment",
                    "Consider using groundhog for date-based package versions",
                    "Be careful with compiled packages that may be OS-specific"
                ]
            },
            "python": {
                "environment": "Use virtual environments or conda",
                "requirements": "Create requirements.txt with specific versions",
                "tips": [
                    "Use pip freeze > requirements.txt",
                    "Consider poetry or pipenv for dependency management",
                    "Be explicit about Python version (3.8, 3.9, etc.)"
                ]
            },
            "containers": {
                "docker": "Provides complete environment reproducibility",
                "singularity": "Often preferred in HPC environments",
                "tips": [
                    "Start with a minimal base image",
                    "Document the build process",
                    "Consider size and accessibility"
                ]
            }
        }
        
        self.common_issues = {
            "path_problems": {
                "issue": "Hard-coded paths that won't work on other systems",
                "solution": "Use relative paths or configurable path variables"
            },
            "missing_data": {
                "issue": "Data files not included or accessible",
                "solution": "Provide data or clear instructions for access"
            },
            "undocumented_dependencies": {
                "issue": "Required packages or software not listed",
                "solution": "Document all requirements explicitly"
            },
            "order_dependency": {
                "issue": "Code must run in specific order not documented",
                "solution": "Number files or provide a master script"
            },
            "random_seeds": {
                "issue": "Results vary due to randomization",
                "solution": "Set random seeds explicitly"
            }
        }
        
        self.repository_guidance = {
            "zenodo": "Excellent for long-term preservation, provides DOI",
            "openicpsr": "AEA's preferred repository, good for economics data",
            "dataverse": "Harvard Dataverse, widely used in social sciences",
            "osf": "Open Science Framework, good for complete projects",
            "github": "Good for code, not for data preservation"
        }
        
        self.documentation_standards = {
            "readme_essential": [
                "Software requirements with versions",
                "Data availability statement",
                "Instructions to run the code",
                "Expected runtime",
                "Hardware requirements if substantial",
                "Description of output"
            ],
            "folder_structure": [
                "Separate raw data from processed data",
                "Keep code organized by purpose",
                "Store output separately",
                "Include documentation folder"
            ]
        }
        
    def initialize_personality_traits(self):
        """Initialize personality traits based on analysis"""
        
        self.communication_style = {
            "teaching": [
                "Let me break this down step by step",
                "Here's how I think about this",
                "In my experience with thousands of replication packages",
                "The key insight here is"
            ],
            "empathy": [
                "I understand this can be challenging",
                "Many researchers face this issue",
                "You're not alone in finding this difficult",
                "This is indeed a complex topic"
            ],
            "encouragement": [
                "You're on the right track",
                "This is a great step forward",
                "Every improvement matters",
                "Perfect is the enemy of good"
            ],
            "pragmatism": [
                "Let's focus on what's practical",
                "Sometimes we need to compromise",
                "Do what you can with the resources you have",
                "Start simple and build from there"
            ]
        }
        
        self.response_patterns = {
            "acknowledge_then_explain": True,
            "provide_examples": True,
            "offer_alternatives": True,
            "reference_resources": True,
            "use_we_language": True  # "We can approach this by..."
        }
        
    def assess_user_level(self, message: str) -> str:
        """Assess user's experience level from their message"""
        beginner_indicators = ["new to", "first time", "beginner", "never done", "confused", "help me understand"]
        intermediate_indicators = ["i've tried", "working on", "issue with", "problem with"]
        advanced_indicators = ["optimize", "best practice", "scaling", "automation", "pipeline", "workflow"]
        
        message_lower = message.lower()
        
        if any(ind in message_lower for ind in advanced_indicators):
            return "advanced"
        elif any(ind in message_lower for ind in beginner_indicators):
            return "beginner"
        elif any(ind in message_lower for ind in intermediate_indicators):
            return "intermediate"
        return self.context.user_experience_level
        
    def extract_software_mentions(self, message: str) -> List[str]:
        """Extract software mentions from message"""
        software_patterns = {
            "stata": r'\bstata\b',
            "r": r'\b[rR]\b(?:\s+(?:studio|script|markdown))?',
            "python": r'\bpython\b',
            "matlab": r'\bmatlab\b',
            "julia": r'\bjulia\b',
            "sas": r'\bsas\b',
            "docker": r'\bdocker\b',
            "git": r'\bgit(?:hub)?\b'
        }
        
        mentioned = []
        message_lower = message.lower()
        for software, pattern in software_patterns.items():
            if re.search(pattern, message_lower, re.IGNORECASE):
                mentioned.append(software)
        return mentioned
        
    def generate_contextual_response(self, message: str) -> str:
        """Generate a response considering context and personality"""
        
        # Update context
        self.context.user_experience_level = self.assess_user_level(message)
        software_mentioned = self.extract_software_mentions(message)
        self.context.software_mentioned.extend(software_mentioned)
        self.context.questions_asked.append(message)
        
        message_lower = message.lower()
        response_parts = []
        
        # Handle greetings
        if any(g in message_lower for g in ["hello", "hi", "hey"]) and len(self.context.questions_asked) <= 1:
            intro = f"Hello! I'm Lars Vilhuber, {random.choice(self.roles)}. "
            intro += "I work on making economics research more reproducible and transparent. How can I help you today?"
            return intro
            
        # Acknowledge the question appropriately
        if self.context.user_experience_level == "beginner":
            response_parts.append(random.choice(self.communication_style["empathy"]))
        else:
            response_parts.append(random.choice(["Good question.", "Let me address that.", "Sure, I can help with that."]))
            
        # Main response based on topic detection
        if "computational empathy" in message_lower:
            response_parts.append(self.explain_computational_empathy())
        elif any(word in message_lower for word in ["reproduce", "replication", "package"]):
            response_parts.append(self.discuss_reproducibility())
        elif any(word in message_lower for word in ["data", "access", "confidential", "restricted"]):
            response_parts.append(self.discuss_data_access())
        elif any(word in message_lower for word in ["software", "environment", "version"]):
            response_parts.append(self.discuss_software_environments())
        elif any(word in message_lower for word in ["readme", "document", "organize"]):
            response_parts.append(self.discuss_documentation())
        elif any(word in message_lower for word in ["repository", "archive", "preserve"]):
            response_parts.append(self.discuss_repositories())
        elif "teach" in message_lower or "student" in message_lower:
            response_parts.append(self.discuss_teaching())
        else:
            # General reproducibility advice
            response_parts.append(self.provide_general_guidance())
            
        # Add software-specific advice if mentioned
        if software_mentioned:
            for software in software_mentioned[:1]:  # Limit to avoid too long responses
                if software in self.software_expertise:
                    response_parts.append(f"\\n\\nFor {software.capitalize()} specifically: {random.choice(self.software_expertise[software]['tips'])}")
                    
        # Close with encouragement if beginner
        if self.context.user_experience_level == "beginner":
            response_parts.append(random.choice(self.communication_style["encouragement"]))
            
        return " ".join(response_parts)
        
    def explain_computational_empathy(self) -> str:
        return ("Computational empathy is about putting yourself in the shoes of someone trying to reproduce your work. "
                "They might use a different operating system, have different software versions, or different levels of expertise. "
                "The key is to document everything explicitly and test your code as if you were that person.")
        
    def discuss_reproducibility(self) -> str:
        responses = [
            "Reproducibility starts with good habits: clear file organization, documented dependencies, and tested code. "
            "I recommend the 'run it again' test - delete your output and see if you can recreate everything from scratch.",
            
            "A good replication package has three key elements: all the data (or clear access instructions), "
            "all the code in runnable form, and clear documentation linking the code to the paper results.",
            
            "Think of reproducibility as a ladder - each rung makes your work more accessible. "
            "Start with making it work for you, then a colleague, then someone in your field, then anyone."
        ]
        return random.choice(responses)
        
    def discuss_data_access(self) -> str:
        responses = [
            "When data can't be shared, transparency is still possible. Document the data structure, "
            "provide access instructions, and consider creating synthetic data that demonstrates your code works.",
            
            "Data availability statements should be precise: what data exists, where it can be found, "
            "and what restrictions apply. 'Data available upon request' is not sufficient anymore.",
            
            "Even confidential data can be made reproducible. Document the exact data pulls, "
            "provide code that works with the data structure, and be clear about access procedures."
        ]
        return random.choice(responses)
        
    def discuss_software_environments(self) -> str:
        responses = [
            "Software environments are often the biggest reproducibility challenge. "
            "Always document versions explicitly - for everything from the language itself to every package used.",
            
            "Consider using environment management tools: renv for R, virtual environments for Python, "
            "or containers like Docker for complex setups. They save headaches later.",
            
            "Different journals and archives have different software availability. "
            "Don't assume everyone has access to proprietary software or the latest versions."
        ]
        return random.choice(responses)
        
    def discuss_documentation(self) -> str:
        standards = self.documentation_standards["readme_essential"]
        return (f"Good documentation starts with a clear README. Essential elements include: "
                f"{', '.join(standards[:3])}, and more. "
                "Think of it as a letter to a stranger who needs to understand your work.")
        
    def discuss_repositories(self) -> str:
        return ("For long-term preservation, use trusted repositories. "
                f"{random.choice(list(self.repository_guidance.keys())).capitalize()} is "
                f"{self.repository_guidance[random.choice(list(self.repository_guidance.keys()))]}. "
                "GitHub is great for collaboration but isn't an archive.")
        
    def discuss_teaching(self) -> str:
        return ("Teaching reproducibility is crucial for the next generation. "
                "I recommend starting with simple exercises - have students reproduce a basic analysis, "
                "then gradually introduce complications. The 'have an undergrad run it' test is remarkably effective!")
        
    def provide_general_guidance(self) -> str:
        guidance_options = [
            "Start with small steps toward reproducibility. Even documenting your software versions is progress.",
            "Remember, perfect is the enemy of good. Any documentation is better than none.",
            "Focus on making your future self happy - good reproducibility practices save you time too.",
            "The reproducibility community is supportive. We're all learning and improving together."
        ]
        return random.choice(guidance_options)
        
    def chat(self):
        """Run the interactive chat session"""
        print("\\n" + "="*70)
        print("Advanced Lars Vilhuber Chatbot")
        print("Expert in Reproducibility and Data Transparency in Economics")
        print("Type 'quit' to exit | 'reset' to start fresh | 'help' for guidance")
        print("="*70 + "\\n")
        
        print(self.generate_contextual_response("Hello"))
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\\nLars: It was great talking with you! Remember, every step toward reproducibility matters. "
                          f"Feel free to check out my self-checking reproducibility guide on GitHub for more tips. Good luck with your research!")
                    break
                    
                if user_input.lower() == 'reset':
                    self.context = ResearchContext()
                    print("\\nLars: Let's start fresh. What would you like to discuss?")
                    continue
                    
                if user_input.lower() == 'help':
                    print("\\nLars: I can help with:")
                    print("  • Reproducibility and replication packages")
                    print("  • Data transparency and confidential data")
                    print("  • Software environments and dependencies")
                    print("  • Documentation standards and best practices")
                    print("  • Repository choices and data preservation")
                    print("  • Teaching reproducibility")
                    print("\\nJust ask me about any of these topics!\\n")
                    continue
                    
                if not user_input:
                    continue
                    
                response = self.generate_contextual_response(user_input)
                print(f"\\nLars: {response}\\n")
                
            except KeyboardInterrupt:
                print("\\n\\nLars: Thanks for the conversation! Keep working on reproducibility!")
                break
            except Exception as e:
                print(f"\\nLars: I apologize, could you rephrase that? I want to make sure I understand correctly.")
                continue

def main():
    chatbot = LarsVilhuberAdvancedChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()