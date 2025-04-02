# TalentScout Hiring Assistant

## Project Overview
TalentScout Hiring Assistant is an intelligent chatbot designed to streamline the initial screening process for technical candidates. The chatbot helps recruitment agencies by automating the collection of candidate information and conducting preliminary technical assessments based on the candidate's declared tech stack.

## Key Features
- **Information Collection:** Gathers essential candidate details including name, contact info, experience, and desired positions.
- **Tech Stack Assessment:** Asks candidates to specify their technical skills.
- **Dynamic Question Generation:** Creates tailored technical questions based on the candidate's tech stack.
- **Coherent Conversation Flow:** Maintains context throughout the interaction.
- **User-Friendly Interface:** Clean and intuitive Streamlit UI for seamless interaction.
- **Data Export:** Ability to export conversation data for further analysis.

## Installation Instructions

### Clone the repository
```sh
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
```

### Create a virtual environment
```sh
python -m venv venv
```

### Activate the virtual environment
**Windows:**
```sh
venv\Scripts\activate
```
**Mac/Linux:**
```sh
source venv/bin/activate
```

### Install dependencies
```sh
pip install -r requirements.txt
```

### Set up your OpenAI API key
Open `config.py` and replace `"your-api-key-here"` with your actual OpenAI API key.
Alternatively, create a `.env` file with:
```sh
OPENAI_API_KEY=your-actual-api-key
```

### Run the application
```sh
streamlit run app.py
```

## Usage Guide

### Start the application
- Click the **"Start Conversation"** button to begin the interview process.

### Candidate Information Collection
- The chatbot will guide you through providing personal information.
- Required details include: name, email, phone, experience, desired position, location, and tech stack.

### Technical Assessment
- Based on your tech stack, the chatbot will generate relevant technical questions.
- Answer the questions to complete the assessment.

### End the Conversation
- Type `exit`, `bye`, `quit`, or `end` to conclude the interview.
- Once finished, you can download the conversation data as a JSON file.

### Reset the Conversation
- Use the **"Reset Conversation"** button to start over.

## Technical Details

### Architecture
- **Frontend:** Streamlit for the user interface.
- **Backend Logic:** Python for conversation management and LLM integration.
- **LLM Integration:** OpenAI GPT API for natural language processing.

### Libraries Used
- `streamlit`: Web application framework.
- `openai`: Integration with OpenAI's language models.
- `python-dotenv`: Environment variable management.
- **Standard Python libraries:** `json`, `re`, `datetime`, etc.

### Files Structure
- **`app.py`**: Main Streamlit application entry point.
- **`chatbot.py`**: Conversation management and LLM integration.
- **`config.py`**: Configuration settings and prompts.
- **`utils.py`**: Utility functions for data validation and formatting.
- **`requirements.txt`**: Project dependencies.

## Prompt Design
The prompt engineering approach focuses on guiding the LLM through a structured conversation flow:

### System Prompt
- Sets the context and defines the chatbot's purpose and behavior.
- Clearly outlines the information collection sequence.
- Establishes the technical assessment workflow.
- Maintains a professional yet friendly tone.

### Information Collection Prompts
- Direct prompts for gathering specific candidate details.
- Each field has a dedicated prompt to ensure clarity.
- Includes validation for critical fields like email and phone.

### Tech Question Generation Prompt
- Dynamic prompt that adapts to the candidate's tech stack.
- Uses the candidate's declared skills to generate relevant questions.
- Ensures questions cover fundamental to advanced concepts.
- Balances theoretical knowledge and practical application questions.

## Challenges & Solutions

### Challenge 1: Maintaining Conversation Context
**Solution:** Implemented a state-based conversation manager that tracks the current state and manages the flow of conversation, ensuring that the chatbot always knows where it is in the process and what information it has already collected.

### Challenge 2: Generating Relevant Technical Questions
**Solution:** Crafted a specialized prompt that dynamically incorporates the candidate's tech stack and provides clear instructions to the LLM about the types and depth of questions to generate.

### Challenge 3: Handling Invalid Inputs
**Solution:** Added validation functions for critical fields like email and phone number, with feedback loops that ask the candidate to correct invalid inputs.

### Challenge 4: User Experience Design
**Solution:** Designed a clean Streamlit interface with custom CSS for better visual hierarchy, clear message attribution, and timestamps to improve readability and usability.

### Challenge 5: Error Handling and Resilience
**Solution:** Implemented retry logic for API calls and graceful fallbacks in case of service disruptions to ensure the application remains functional even when facing external issues.

## Future Enhancements
- **Sentiment Analysis:** Detect candidate emotions during the interview.
- **Multilingual Support:** Conduct interviews in multiple languages.
- **Customizable Question Difficulty:** Adjust technical questions based on seniority level.
- **Video Integration:** Add an option for video responses to certain questions.
- **Enhanced Analytics:** Provide detailed analysis of candidate responses.

## License
This project is created for educational purposes as part of an assignment.

This project was developed for the AI/ML Intern Assignment for TalentScout recruitment agency.