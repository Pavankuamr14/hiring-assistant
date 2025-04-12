"""
Configuration settings for the TalentScout Hiring Assistant application.
"""
import os  
from dotenv import load_dotenv  

load_dotenv()  
import streamlit as st

# Load API key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Gemini API configuration

# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  

GEMINI_MODEL = "gemini-1.5-pro-latest"  # Adjust to the appropriate model

# System prompt for the chatbot
SYSTEM_PROMPT = """
You are a hiring assistant for TalentScout, a tech recruitment agency specializing in technology placements.
Your purpose is to conduct initial candidate screening by:
1. Collecting essential candidate information
2. Asking relevant technical questions based on the candidate's declared tech stack
3. Maintaining a professional, friendly, and coherent conversation

You should gather the following information in this order:
- Full Name
- Email Address
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack (programming languages, frameworks, databases, tools they are proficient in)

After collecting the tech stack information, generate 3-5 technical questions tailored to assess 
the candidate's proficiency in their specified technologies.

Stay focused on the hiring process and maintain context. If the candidate asks questions unrelated 
to the interview process, politely redirect them back to the screening process.

End the conversation when the candidate says "exit", "quit", "bye", or "end".
"""

# Exit keywords to end the conversation
EXIT_KEYWORDS = ["exit", "quit", "bye", "end", "goodbye"]

# Required candidate information fields
REQUIRED_INFO = [
    "name",
    "email",
    "phone",
    "experience",
    "position",
    "location",
    "tech_stack"
]

# Information collection prompts
INFO_PROMPTS = {
    "name": "Let's start the screening process. Could you please provide your full name?",
    "email": "Thank you. Now, could you please share your email address?",
    "phone": "Great! Could you provide your phone number?",
    "experience": "How many years of professional experience do you have?",
    "position": "What position(s) are you interested in applying for?",
    "location": "What is your current location?",
    "tech_stack": "Please list the technologies you're proficient in, including programming languages, frameworks, databases, and tools."
}

# Confirmation messages
CONFIRMATION_MESSAGE = "Thank you for providing your information. Let me summarize what you've shared:"

# Technical question generation prompt template
TECH_QUESTION_PROMPT = """
Based on the candidate's tech stack: {tech_stack}

Generate 3-5 relevant technical questions to assess their proficiency in these technologies. 
The questions should:
1. Be specific to the mentioned technologies
2. Range from fundamental to advanced concepts
3. Include scenario-based questions where appropriate
4. Assess both theoretical knowledge and practical application

For each technology mentioned, provide at least one question. Focus more questions on the candidate's 
primary technologies if they have indicated any preferences.
"""

# Closing message
CLOSING_MESSAGE = """
Thank you for completing the initial screening process with TalentScout. We've collected your information and assessed your technical knowledge. Our recruitment team will review your responses and get back to you soon if there's a potential match. 

If you have any questions about your application or the recruitment process, feel free to reach out to us at recruiter@talentscout.fictional.

Have a great day!
"""