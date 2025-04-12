import streamlit as st
import re
import time
import json
import os
from datetime import datetime
from chatbot import ConversationManager
from config import EXIT_KEYWORDS

# Set page config
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="👔",
    layout="centered"
)

# Custom CSS for better UI with text wrapping fixes and better color contrast
st.markdown("""
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}
.chat-message.user {
    background-color: #F0F2F6;
    border-left: 5px solid #7E57C2;
    color: #111; /* Dark text for light backgrounds */
}
.chat-message.assistant {
    background-color: #FAFAFA;
    border-left: 5px solid #26A69A;
    color: #111; /* Dark text for light backgrounds */
}
.chat-message .message-content {
    display: flex;
    margin-top: 0;
    /* Fix for text wrapping */
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.message-timestamp {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.2rem;
}
.visually-hidden {
    display: none;
}
div.stButton > button {
    width: 100%;
}
/* Improved Technical Question Styling with text wrapping fixes */
.technical-question-container {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 0.5rem;
    border-left: 5px solid #3498db;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    /* Fix for text wrapping */
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.technical-question-text {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #2c3e50;
    margin: 0;
    padding: 0;
    text-align: left;
    /* Fix for text wrapping */
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
/* Styling for text areas */
.stTextArea textarea {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    font-size: 1rem;
    line-height: 1.5;
    resize: vertical;
    /* Fix for text wrapping */
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
/* Button styling */
.stButton button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.3s;
}
.stButton button:hover {
    background-color: #2980b9;
}
/* Success message styling */
.stSuccess {
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 5px;
    border-left: 5px solid #28a745;
    margin-bottom: 1rem;
}
/* Global text wrapping styles */
p, div, span, h1, h2, h3, h4, h5, h6 {
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}
/* Fix for markdown content */
.markdown-text-container {
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}
/* Force Streamlit elements to wrap properly */
.element-container, .stMarkdown, .stText {
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)


def initialize_session():
    """Initialize session state variables."""
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'session_started' not in st.session_state:
        st.session_state.session_started = False
    if 'conversation_ended' not in st.session_state:
        st.session_state.conversation_ended = False
    if 'technical_responses_input' not in st.session_state:
        st.session_state.technical_responses_input = {}
    if 'technical_questions' not in st.session_state:
        st.session_state.technical_questions = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'reviewing_answers' not in st.session_state:
        st.session_state.reviewing_answers = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            "name": "",
            "email": "",
            "phone": "",
            "experience": "",
            "tech_stack": [],
            
            "submission_time": "",
            "interview_status": "incomplete"
        }


def display_message(role, content, timestamp=None):
    """
    Display a chat message with styling based on the role.
    Args:
        role: 'user' or 'assistant'
        content: Message content
        timestamp: Optional timestamp for the message
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")
    # Ensure content is properly formatted for HTML
    content = content.replace("\n", "<br>")
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div class="message-content">
                <b>You:</b> {content}
            </div>
            <div class="message-timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant">
            <div class="message-content">
                <b>Hiring Assistant:</b> {content}
            </div>
            <div class="message-timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
def extract_user_data(text):
    """
    Extract user data from text using keyword detection and simple heuristics.
    Returns a dictionary of extracted user data.
    """
    extracted_data = {}
    text_lower = text.lower().strip()
    
    # First check if this is a direct response to a specific question based on context
    # This helps prevent overwriting previously collected data
    
    # Check if this is a response to "What position(s) are you interested in applying for?"
    position_question_patterns = [
        "what position", "which position", "what role", "which role", 
        "interested in applying", "looking to apply"
    ]
    position_response = any(pattern in text_lower for pattern in position_question_patterns)
    
    # Check if this is a response to "Could you please provide your full name?"
    name_question_patterns = [
        "your name", "full name", "provide name", "what is your name", 
        "introduce yourself", "who are you"
    ]
    name_response = any(pattern in text_lower for pattern in name_question_patterns)
    
    # ======== Extract Position (if this is a position response) ========
    if position_response:
        # If this is a direct answer to position question, treat entire input as position
        extracted_data["desired_position"] = text.strip()
        # Skip name extraction in this case to prevent overwriting
        return extracted_data
    
    # ======== Extract Name ========
    # Check if this is likely a direct name response
    if name_response or (len(text.split()) <= 3 and all(word.isalpha() for word in text.split())):
        # Common job/tech terms that should not be treated as names
        common_tech_terms = [
            "python", "java", "javascript", "typescript", "developer", "engineer", 
            "frontend", "backend", "fullstack", "machine learning", "data science",
            "devops", "cloud", "architect", "analyst", "security", "designer",
            "manager", "lead", "senior", "junior", "mid", "level", "software"
        ]
        
        # Only consider it a name if it doesn't contain common tech terms
        if not any(term in text_lower for term in common_tech_terms):
            extracted_data["name"] = text.strip()
    
    # Special case for "my name is" format
    elif "my name is" in text_lower:
        name_start = text_lower.find("my name is") + len("my name is")
        name_end = text_lower.find(".", name_start)
        if name_end == -1:  # If no period found, try finding other punctuation or end of string
            other_punctuation = [",", "\n", ";"]
            end_positions = [text_lower.find(p, name_start) for p in other_punctuation]
            # Filter out -1 positions (not found)
            end_positions = [pos for pos in end_positions if pos != -1]
            # Add end of string as a possible endpoint
            end_positions.append(len(text_lower))
            # Take the earliest position as the end point
            name_end = min(end_positions) if end_positions else len(text_lower)
        
        name = text[name_start:name_end].strip()
        if name:
            extracted_data["name"] = name

    # Key-value format
    elif "name:" in text_lower:
        name_start = text_lower.find("name:") + len("name:")
        name_end = text_lower.find("\n", name_start)
        if name_end == -1:
            name_end = len(text)
        name = text[name_start:name_end].strip()
        if name:
            extracted_data["name"] = name

    # ======== Extract Email ========
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, text)
    if email_matches:
        extracted_data["email"] = email_matches[0].lower()

    # ======== Extract Phone ========
    phone_pattern = r'(\+\d{1,3}[-.\s]?)?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}|\d{10})'
    phone_matches = re.findall(phone_pattern, text)
    if phone_matches:
        phone = ''.join(filter(None, phone_matches[0]))
        phone = re.sub(r'[^\d+]', '', phone)
        extracted_data["phone"] = phone

    # ======== Extract Experience ========
    exp_keywords = ["years of experience", "years experience", "year experience", "years in"]
    found_exp = False
    for keyword in exp_keywords:
        if keyword in text_lower:
            match = re.search(r'(\d+)\s+' + re.escape(keyword), text_lower)
            if match:
                extracted_data["experience"] = match.group(1) + " years"
                found_exp = True
                break

    # Standalone experience like "3", "3 years", "4 yrs"
    if not found_exp and text_lower.strip().isdigit():
        extracted_data["experience"] = text.strip() + " years"

    # ======== Extract Desired Position ========
    # Only extract position if not already handled by direct response logic above
    if "desired_position" not in extracted_data:
        position_patterns = [
            r'(position|role|job)(\s*[:\-]?\s*)([a-zA-Z ]+)',
            r'(applying for|interested in)(\s+[a-z]*)?\s+([a-zA-Z ]+developer|[a-zA-Z ]+engineer|[a-zA-Z ]+designer)'
        ]
        
        for pattern in position_patterns:
            match = re.search(pattern, text_lower)
            if match:
                position = match.group(3).strip().rstrip('.')
                extracted_data["desired_position"] = position
                break

    # ======== Extract Tech Stack ========
    tech_keywords = [
        "python", "javascript", "java", "c#", "c++", "ruby", "php", "swift", "kotlin", "go", "rust", "typescript",
        "html", "css", "react", "angular", "vue", "node", "django", "flask", "spring",
        "aws", "azure", "gcp", "docker", "kubernetes", "sql", "nosql",
        "mongodb", "postgresql", "mysql", "redis", "tensorflow", "pytorch", "machine learning"
    ]

    found_techs = [tech for tech in tech_keywords if re.search(r'\b' + re.escape(tech) + r'\b', text_lower)]
    if found_techs:
        extracted_data["tech_stack"] = found_techs

    return extracted_data
def update_user_data(extracted_data):
    """
    Update Streamlit session_state with extracted user data.
    Merges tech stack and updates other fields without overwriting existing data.
    """
    for key, value in extracted_data.items():
        # Always merge tech stack
        if key == "tech_stack" and isinstance(value, list):
            existing_stack = st.session_state.user_data.get(key, [])
            st.session_state.user_data[key] = list(set(existing_stack + value))
        # Don't overwrite name if it already exists
        elif key == "name" and st.session_state.user_data.get("name") and value:
            # Only update if the existing name is very short (likely incomplete)
            if len(st.session_state.user_data["name"].split()) < len(value.split()):
                st.session_state.user_data[key] = value
        # For other fields, only update if the value is meaningful
        elif value:
            st.session_state.user_data[key] = value
def save_user_data():
    """
    Save the user data to a JSON file.
    Creates a directory if it doesn't exist and names the file using email, name, or timestamp.
    Format: EMAIL_YYYYMMDD_HHMMSS.json (e.g., pavan@gmail.com_20250412_072201.json)
    Uses underscores as separators for Windows compatibility.
    """
    # Create directory if it doesn't exist
    data_dir = "user_data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Prepare data for saving
    user_data = st.session_state.user_data.copy()
    
    # Get current timestamp for submission time and filename
    current_time = datetime.now()
    user_data["submission_time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Format timestamp for filename in the requested format: YYYYMMDD_HHMMSS
    date_str = current_time.strftime('%Y%m%d')
    time_str = current_time.strftime('%H%M%S')

    # Add technical responses
    if st.session_state.technical_responses_input:
        technical_responses = {}
        for i, question in enumerate(st.session_state.technical_questions):
            response_key = f"response_{i}"
            if response_key in st.session_state.technical_responses_input:
                technical_responses[f"question_{i+1}"] = {
                    "question": question,
                    "answer": st.session_state.technical_responses_input[response_key]
                }
        user_data["technical_responses"] = technical_responses

    # Determine file name based on the requested format
    if "email" in user_data and user_data["email"]:
        # Convert email to lowercase as requested
        email = user_data["email"].lower()
        # Replace @ with "_at_" for better Windows compatibility
        email = email.replace("@", "@")
        # but it's not a good idea to use "@" in filenames, so we will replace it with "_at_"
        filename = f"{email}_{date_str}_{time_str}.json"
    elif "name" in user_data and user_data["name"]:
        # Fallback to name-based filename if email is not available
        name_part = user_data["name"].lower().replace(" ", "_")
        filename = f"{name_part}_{date_str}_{time_str}.json"
    else:
        # Last resort fallback
        filename = f"candidate_{date_str}_{time_str}.json"

    # Save to file
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'w') as f:
        json.dump(user_data, f, indent=4)

    return file_path

def handle_user_input():
    """Process user input from the text input field."""
    user_input = st.session_state.user_input
    if user_input:
        # Check for exit keywords
        if any(keyword in user_input.lower() for keyword in EXIT_KEYWORDS):
            st.session_state.conversation_ended = True
            # Gracefully conclude the conversation
            timestamp = datetime.now().strftime("%H:%M:%S")
            goodbye_message = (
                "Thank you for taking the time to complete this interview. "
                "We appreciate your interest in joining our team. We will review your responses "
                "and get back to you shortly regarding the next steps."
            )
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": goodbye_message,
                "timestamp": timestamp
            })
            st.session_state.user_data["interview_status"] = "complete"
            save_user_data()
            st.session_state.user_input = ""
            return

        # Extract user data from input
        extracted_data = extract_user_data(user_input)
        update_user_data(extracted_data)

        # Add user message to chat history
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })

        # Process input and get response if conversation is active
        if not st.session_state.conversation_ended:
            # Display thinking indicator
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("*Thinking...*")
            # Get response from conversation manager
            response = st.session_state.conversation_manager.process_input(user_input)
            # Remove thinking indicator
            thinking_placeholder.empty()

            # Process the response to extract technical questions if present
            if "Here are your technical questions:" in response:
                # Extract technical questions from the response
                # Split response at the technical questions marker
                clean_response = response.split("Here are your technical questions:")[0]
                clean_response += "I've prepared some technical questions for you. I'll present them one by one."
                # Add the modified response to chat history
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": clean_response,
                    "timestamp": timestamp
                })
                
                # Parse the questions and store them - IMPROVED VERSION
                questions_part = response.split("Here are your technical questions:")[1]
                
                # Improved regex to capture complete questions including the assessment notes
                import re
                
                # Extract questions - improved pattern to capture full questions
                questions = []
                # Split by numbered items
                question_blocks = re.split(r'(\d+\.)', questions_part.strip())
                if len(question_blocks) > 1:  # Skip the first empty item if present
                    i = 1
                    while i < len(question_blocks):
                        if re.match(r'\d+\.', question_blocks[i]) and i+1 < len(question_blocks):
                            # Combine number with text
                            full_question = question_blocks[i] + question_blocks[i+1].strip()
                            questions.append(full_question)
                            i += 2
                        else:
                            i += 1
                
                # If the regex method failed, try a simpler approach
                if not questions:
                    question_lines = [line.strip() for line in questions_part.split('\n') if line.strip()]
                    questions = []
                    current_question = ""
                    for line in question_lines:
                        if re.match(r'^\d+\.', line):
                            if current_question:
                                questions.append(current_question)
                            current_question = line
                        elif current_question:
                            current_question += " " + line
                    if current_question:
                        questions.append(current_question)
                
                # Clean up and store questions
                clean_questions = []
                for q in questions:
                    # Remove assessment markers if needed but keep the main question
                    # Extract just the question part from "1. **Question text** (Assessment note)"
                    match = re.match(r'\d+\.\s+\*\*(.*?)\*\*\s*(?:\(.*?\))?', q)
                    if match:
                        clean_questions.append(match.group(1))
                    else:
                        # If no match, just use the whole question with minimal cleaning
                        clean_q = re.sub(r'^\d+\.\s+', '', q)
                        clean_questions.append(clean_q)
                
                # Store only if we have valid questions
                if clean_questions:
                    st.session_state.technical_questions = clean_questions
            else:
                # Regular response without technical questions
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": timestamp
                })

            # Check if conversation has ended
            if not st.session_state.conversation_manager.is_active:
                st.session_state.conversation_ended = True
                # Save conversation summary
                summary = st.session_state.conversation_manager.get_conversation_summary()
                st.session_state.conversation_summary = summary
                # Update user data from summary if available
                if "candidate_info" in summary:
                    for key, value in summary["candidate_info"].items():
                        if key in st.session_state.user_data and value:
                            st.session_state.user_data[key] = value
                # Mark interview as complete
                st.session_state.user_data["interview_status"] = "complete"
                # Save user data to file
                save_user_data()

        # Clear input field
        st.session_state.user_input = ""


def start_session():
    """Start a new chat session."""
    st.session_state.session_started = True
    # Add initial greeting
    greeting = st.session_state.conversation_manager.process_input("Hello")
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": greeting,
        "timestamp": timestamp
    })


def reset_session():
    """Reset the chat session."""
    # Save data before resetting if interview was in progress
    if st.session_state.get('session_started', False) and not st.session_state.get('conversation_ended', False):
        st.session_state.user_data["interview_status"] = "abandoned"
        save_user_data()
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session()


def export_conversation():
    """Export the conversation to a JSON file."""
    # Create conversation data
    if 'conversation_summary' in st.session_state:
        export_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "candidate_info": st.session_state.conversation_summary["candidate_info"],
            "technical_questions": st.session_state.conversation_summary["technical_questions"],
            "technical_responses": st.session_state.conversation_summary["technical_responses"],
            "full_conversation": [
                {
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"]
                } for msg in st.session_state.chat_history
            ]
        }
        # Convert to JSON
        export_json = json.dumps(export_data, indent=2)
        # Create download button
        st.download_button(
            label="Download Conversation Data",
            data=export_json,
            file_name=f"talentscout_interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


def display_technical_questions():
    """Display technical questions one by one with input fields for answers."""
    if not st.session_state.technical_questions:
        return
    if st.session_state.current_question_index < len(st.session_state.technical_questions):
        # Get the current question
        question = st.session_state.technical_questions[st.session_state.current_question_index]
        response_key = f"response_{st.session_state.current_question_index}"
        # Add spacing and format the question
        st.markdown("---")
        st.subheader(f"Technical Question {st.session_state.current_question_index + 1}")
        # Format the question text properly with improved CSS
        st.markdown(f"""
        <div class="technical-question-container">
            <p class="technical-question-text">{question}</p>
        </div>
        """, unsafe_allow_html=True)
        # Use text_area with increased height for better user experience
        st.text_area(
            "Your Answer:",
            key=response_key,
            height=200,
            label_visibility="visible"
        )
        # Use a single button to navigate
        if st.button("Submit Answer"):
            # Store the answer in session state
            st.session_state.technical_responses_input[response_key] = st.session_state[response_key]
            st.session_state.current_question_index += 1
            st.rerun()
    elif st.session_state.technical_questions and st.session_state.current_question_index >= len(st.session_state.technical_questions):
        # Show a message when all questions are answered
        st.markdown("---")
        st.success("You've completed all the technical questions. Thank you! Click on the Save My Data button to save your responses.")
        # Add a button to review answers
        if st.button("Review All Answers"):
            st.session_state.reviewing_answers = True
        # Display review if requested
        if st.session_state.get('reviewing_answers', False):
            st.markdown("## Your Answers")
            for i, question in enumerate(st.session_state.technical_questions):
                response_key = f"response_{i}"
                st.markdown(f"**Question {i+1}:** {question}")
                st.markdown(f"**Your Answer:** {st.session_state.technical_responses_input.get(response_key, '')}")
                st.markdown("---")


def save_user_data_manually():
    """
    Function to manually save user data on demand.
    This can be triggered by a button in the UI.
    """
    if st.session_state.user_data:
        st.session_state.user_data["submission_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = save_user_data()
        st.success(f"User data saved to {file_path}")


def main():
    """Main application function."""
    # Initialize session
    initialize_session()
    # Header
    st.title("🤖 TalentScout Hiring Assistant")
    st.markdown("""
    Welcome to the TalentScout Hiring Assistant. This chatbot will guide you through an initial screening process 
    for technical positions. It will collect your information and ask technical questions based on your skills.
    """)
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This hiring assistant helps TalentScout recruitment agency screen candidates for technical positions.
        **The assistant will:**
        - Collect your personal information
        - Ask about your tech stack
        - Pose technical questions based on your skills
        Your responses will be evaluated for potential job matches.
        """)
        st.header("Controls")
        if not st.session_state.session_started:
            st.button("Start Conversation", on_click=start_session)
        else:
            st.button("Reset Conversation", on_click=reset_session)
            # Add a button to manually save data
            if st.button("Save My Data"):
                save_user_data_manually()
        
        # Display current user data in sidebar for debugging/verification
        if st.session_state.session_started:
            st.header("Current User Data")
            with st.expander("View Details", expanded=True):
                for key, value in st.session_state.user_data.items():
                    if key != "technical_responses":
                        if isinstance(value, list):
                            st.write(f"**{key.replace('_', ' ').title()}:** {', '.join(value)}")
                        else:
                            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        if st.session_state.conversation_ended and 'conversation_summary' in st.session_state:
            st.header("Export")
            export_conversation()

    # Chat container
    chat_container = st.container()

    # Display chat messages
    with chat_container:
        if st.session_state.session_started:
            for message in st.session_state.chat_history:
                display_message(
                    role=message["role"],
                    content=message["content"],
                    timestamp=message["timestamp"]
                )
            display_technical_questions()
            # Show summary if conversation ended
            if st.session_state.conversation_ended and 'conversation_summary' in st.session_state:
                st.markdown("---")
                st.subheader("Conversation Summary")
                with st.expander("Candidate Information", expanded=True):
                    candidate_info = st.session_state.conversation_summary["candidate_info"]
                    for key, value in candidate_info.items():
                        if key == 'tech_stack' and isinstance(value, list):
                            st.text_input(f"{key.title()}", ", ".join(value), disabled=True)
                        else:
                            st.text_input(f"{key.title()}", value, disabled=True)
                with st.expander("Technical Assessment", expanded=True):
                    st.markdown("<div class='markdown-text-container'>", unsafe_allow_html=True)
                    st.markdown("**Questions:**")
                    st.markdown(st.session_state.conversation_summary["technical_questions"])
                    st.markdown("**Responses:**")
                    st.markdown(st.session_state.conversation_summary["technical_responses"])
                    st.markdown("</div>", unsafe_allow_html=True)

    # Input area
    if st.session_state.session_started and not st.session_state.conversation_ended:
        st.text_input(
            "Your message:",
            key="user_input",
            on_change=handle_user_input
        )
        st.markdown("*Press Enter to send your message. Type 'exit' or 'bye' to end the conversation.*")


if __name__ == "__main__":
    main()