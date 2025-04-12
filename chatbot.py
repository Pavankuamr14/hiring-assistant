"""
Chatbot logic for the TalentScout Hiring Assistant.
"""
import os
import subprocess

# Ensure required packages are installed
required_packages = ["python-dotenv", "google-generativeai"]

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))  # Try importing the package
    except ImportError:
        subprocess.run(["pip", "install", package])

import google.generativeai as genai  # Now import your required module

import time
from typing import Dict, List, Tuple, Any, Optional


from config import (
    GEMINI_API_KEY, 
    GEMINI_MODEL, 
    SYSTEM_PROMPT, 
    EXIT_KEYWORDS,
    REQUIRED_INFO,
    INFO_PROMPTS,
    CONFIRMATION_MESSAGE,
    TECH_QUESTION_PROMPT,
    CLOSING_MESSAGE
)
from utils import (
    validate_email, 
    validate_phone, 
    format_candidate_summary,
    check_exit_keywords,
    parse_tech_stack
)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

class ConversationManager:
    """
    Manages the conversation state and flow for the hiring assistant chatbot.
    """
    
    def __init__(self):
        """Initialize the conversation manager."""
        # Initialize conversation state and history
        self.state = "greeting"
        self.current_info_field = None
        self.candidate_info = {}
        self.technical_questions = []
        self.conversation_history = []
        
        # Initialize the model
        self.model = genai.GenerativeModel(model_name=GEMINI_MODEL)
        
        # Add system message to conversation history
        self.conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })
        
        # Store candidate responses to technical questions
        self.question_responses = {}
        
        # Set conversation to active
        self.is_active = True

    def process_input(self, user_input: str) -> str:
        """
        Process user input based on current conversation state.
        
        Args:
            user_input: Text input from the user
            
        Returns:
            str: Response from the chatbot
        """
        # Check for exit keywords
        if check_exit_keywords(user_input, EXIT_KEYWORDS):
            self.is_active = False
            return "Thank you for your time. The conversation has ended."
        
        # Add user input to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Process based on current state
        if self.state == "greeting":
            response = self._handle_greeting()
        elif self.state == "collecting_info":
            response = self._collect_candidate_info(user_input)
        elif self.state == "confirming_info":
            response = self._confirm_info(user_input)
        elif self.state == "asking_tech_questions":
            response = self._handle_tech_questions(user_input)
        elif self.state == "closing":
            response = self._handle_closing()
        else:
            # Default fallback
            response = self._get_llm_response("Please respond to this message in the context of our conversation.")
        
        # Add response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response

    def _handle_greeting(self) -> str:
        """
        Handle the greeting state.
        
        Returns:
            str: Greeting message
        """
        self.state = "collecting_info"
        self.current_info_field = REQUIRED_INFO[0]
        return INFO_PROMPTS[self.current_info_field]

    def _collect_candidate_info(self, user_input: str) -> str:
        """
        Collect and validate candidate information.
        
        Args:
            user_input: Text input from the user
            
        Returns:
            str: Response or next question
        """
        # Validate current input based on field
        valid_input = True
        
        if self.current_info_field == "email":
            if not validate_email(user_input):
                return "That doesn't appear to be a valid email address. Please provide a valid email."
            
        elif self.current_info_field == "phone":
            if not validate_phone(user_input):
                return "That doesn't appear to be a valid phone number. Please provide a valid phone number."
        
        # Store the validated information
        if self.current_info_field == "tech_stack":
            self.candidate_info[self.current_info_field] = parse_tech_stack(user_input)
        else:
            self.candidate_info[self.current_info_field] = user_input
        
        # Move to next field or next state
        current_index = REQUIRED_INFO.index(self.current_info_field)
        if current_index < len(REQUIRED_INFO) - 1:
            # Move to the next field
            self.current_info_field = REQUIRED_INFO[current_index + 1]
            return INFO_PROMPTS[self.current_info_field]
        else:
            # All required info collected, move to confirmation
            self.state = "confirming_info"
            summary = format_candidate_summary(self.candidate_info)
            return f"{CONFIRMATION_MESSAGE}\n\n{summary}\n\nIs this information correct? (yes/no)"

    def _confirm_info(self, user_input: str) -> str:
        """
        Confirm collected information with candidate.
        
        Args:
            user_input: Text input from the user
            
        Returns:
            str: Response based on confirmation
        """
        if user_input.lower().startswith("y"):
            # Information confirmed, generate technical questions
            self.state = "asking_tech_questions"
            return self._generate_technical_questions()
        else:
            # Information needs correction
            self.state = "collecting_info"
            self.current_info_field = REQUIRED_INFO[0]
            self.candidate_info = {}
            return "Let's start again. " + INFO_PROMPTS[self.current_info_field]

    def _generate_technical_questions(self) -> str:
        """Generate technical questions based on candidate's tech stack."""
        
        # Check if tech_stack exists
        tech_stack = self.candidate_info.get("tech_stack", [])
        
        # Debugging: Print values
        print(f"DEBUG: Tech Stack Received -> {tech_stack}")
        
        if not tech_stack:
            return "I'm unable to generate technical questions because no tech stack information was provided."

        # Convert to a comma-separated string
        tech_stack_str = ", ".join(tech_stack)
        
        # Debugging: Print the formatted prompt
        prompt = TECH_QUESTION_PROMPT.format(tech_stack=tech_stack_str)
        print(f"DEBUG: Prompt Sent to LLM -> {prompt}")

        # Get questions from LLM
        questions_response = self._get_llm_response(prompt)

        # Debugging: Check response
        print(f"DEBUG: LLM Response -> {questions_response}")

        if not questions_response or "I'm having trouble processing" in questions_response:
            return "I'm currently experiencing difficulties in generating technical questions. Please try again later."

        self.technical_questions = questions_response.split("\n")
        return f"Here are your technical questions:\n\n{questions_response}\n\nPlease provide your answers."

    def _handle_tech_questions(self, user_input: str) -> str:
        """
        Handle responses to technical questions.
        
        Args:
            user_input: Text input from the user
            
        Returns:
            str: Response or closing message
        """
        # Store response to technical questions
        self.question_responses["technical_answers"] = user_input
        
        # Move to closing state
        self.state = "closing"
        return self._handle_closing()

    def _handle_closing(self) -> str:
        """
        Handle the closing state.
        
        Returns:
            str: Closing message
        """
        self.is_active = False
        return CLOSING_MESSAGE

    def _get_llm_response(self, prompt: str) -> str:
        """
        Get response from the Gemini language model.
        
        Args:
            prompt: Prompt text for the LLM
            
        Returns:
            str: Response from the LLM or error message
        """
        # Create messages for the API call in Gemini format
        history = []
        
        # Convert history format from OpenAI to Gemini
        for msg in self.conversation_history:
            if msg["role"] == "system":
                # For system prompts, we'll add them to the first user message
                continue
            elif msg["role"] == "user":
                history.append({"role": "user", "parts": [{"text": msg["content"]}]})
            elif msg["role"] == "assistant":
                history.append({"role": "model", "parts": [{"text": msg["content"]}]})
        
        # Add current prompt
        current_prompt = prompt
        if len(history) == 0:
            # If this is the first message, prepend the system prompt
            system_content = next((msg["content"] for msg in self.conversation_history if msg["role"] == "system"), "")
            if system_content:
                current_prompt = f"{system_content}\n\n{prompt}"
            
        try:
            # Make API call with retry logic
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    # Start a chat session if we have history, or generate content for a one-off
                    if history:
                        chat = self.model.start_chat(history=history)
                        response = chat.send_message(current_prompt)
                    else:
                        response = self.model.generate_content(current_prompt)
                    
                    # Extract response content
                    llm_response = response.text.strip()
                    
                    # Debugging log
                    print(f"Gemini Response: {llm_response[:100]}...")  # Log first 100 chars

                    if not llm_response:
                        raise ValueError("Received an empty response from Gemini.")
                    
                    return llm_response


                except Exception as e:
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        wait_time = 2 ** attempt
                        print(f"API Error: {e}. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise e

        except Exception as e:
            print(f"Gemini API call failed: {e}")
            return "I'm currently experiencing difficulties in generating a response. Please try again later."

    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the conversation.
        
        Returns:
            Dict: Summary of candidate information and technical responses
        """
        summary = {
            "candidate_info": self.candidate_info,
            "technical_questions": self.technical_questions,
            "technical_responses": self.question_responses.get("technical_answers", "")
        }
        return summary