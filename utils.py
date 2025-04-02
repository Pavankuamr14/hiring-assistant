"""
Utility functions for the TalentScout Hiring Assistant.
"""

import re
from typing import Dict, List, Any


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email: String containing the email to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    Basic validation - accepts digits, spaces, dashes, parentheses, and plus sign.
    
    Args:
        phone: String containing the phone number to validate
        
    Returns:
        bool: True if phone format is valid, False otherwise
    """
    # Remove all non-digit characters and check if we have at least 7 digits
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 7


def format_candidate_summary(candidate_info: Dict[str, Any]) -> str:
    """
    Format candidate information for display.
    
    Args:
        candidate_info: Dictionary containing candidate information
        
    Returns:
        str: Formatted string with candidate information
    """
    summary = []
    
    if 'name' in candidate_info:
        summary.append(f"Name: {candidate_info['name']}")
    
    if 'email' in candidate_info:
        summary.append(f"Email: {candidate_info['email']}")
    
    if 'phone' in candidate_info:
        summary.append(f"Phone: {candidate_info['phone']}")
    
    if 'experience' in candidate_info:
        summary.append(f"Experience: {candidate_info['experience']}")
    
    if 'position' in candidate_info:
        summary.append(f"Desired Position: {candidate_info['position']}")
    
    if 'location' in candidate_info:
        summary.append(f"Location: {candidate_info['location']}")
    
    if 'tech_stack' in candidate_info:
        tech_stack = candidate_info['tech_stack']
        # If tech_stack is a list, join it with commas
        if isinstance(tech_stack, list):
            tech_stack = ", ".join(tech_stack)
        summary.append(f"Tech Stack: {tech_stack}")
    
    return "\n".join(summary)


def check_exit_keywords(input_text: str, exit_keywords: List[str]) -> bool:
    """
    Check if input contains any exit keywords.
    
    Args:
        input_text: User input text
        exit_keywords: List of words that trigger conversation exit
        
    Returns:
        bool: True if exit keyword found, False otherwise
    """
    input_lower = input_text.lower()
    for keyword in exit_keywords:
        if keyword in input_lower:
            return True
    return False


def parse_tech_stack(tech_stack_text: str) -> List[str]:
    """
    Parse tech stack text into a list of technologies.
    
    Args:
        tech_stack_text: String describing tech stack
        
    Returns:
        List[str]: List of individual technologies
    """
    # Split by commas, semicolons, and "and"
    separators = r'[,;\s]+(?:and\s+)?|\s+and\s+'
    technologies = re.split(separators, tech_stack_text)
    
    # Clean up the technology names
    cleaned_technologies = []
    for tech in technologies:
        tech = tech.strip()
        if tech:  # Check if not empty
            cleaned_technologies.append(tech)
    
    return cleaned_technologies
  
  