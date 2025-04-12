# TalentScout Hiring Assistant

## Project Overview
**TalentScout Hiring Assistant** is an intelligent chatbot built using the Gemini API to automate the initial screening process for technical candidates. It streamlines the hiring workflow by collecting candidate data and dynamically generating technical questions based on their tech stack.

## Key Features
- **Information Collection:** Gathers essential candidate details like name, contact info, experience, and desired position.
- **Tech Stack Assessment:** Identifies technologies and tools the candidate is proficient in.
- **Dynamic Question Generation:** Creates tailored technical questions based on the declared tech stack.
- **Coherent Conversation Flow:** Maintains state throughout the interaction.
- **User-Friendly Interface:** Clean Streamlit UI for smooth user experience.
- **Data Export:** Saves all conversation data to JSON for review and analysis.

---

## Installation Instructions

### Clone the Repository
```sh
git clone https://github.com/Pavankuamr14/hiring-assistant.git
cd hiring-assistant
```

### Create a Virtual Environment
```sh
python -m venv venv
```

### Activate the Virtual Environment
**Windows:**
```sh
venv\Scripts\activate
```
**Mac/Linux:**
```sh
source venv/bin/activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Set Up Your Gemini API Key
Open `config.py` and replace `"your-gemini-api-key"` with your actual Gemini API key.  
Alternatively, create a `.env` file with:
```env
GEMINI_API_KEY=your-actual-api-key
```

---

## Usage Guide

### Start the Application
```sh
streamlit run app.py
```

### Candidate Interaction
- Click **"Start Conversation"** to begin.
- The chatbot will ask for:
  - Name
  - Email
  - Phone number
  - Experience
  - Desired position
  - Location
  - Tech stack

### Technical Assessment
- The bot generates questions based on your tech stack.
- Provide answers directly in the chat interface.

### Finish or Reset
- Type `exit`, `bye`, `quit`, or `end` to finish.
- Use the **"Reset Conversation"** button to restart the process.

---

## Technical Details

### Architecture
- **Frontend:** Streamlit
- **Backend Logic:** Python with Gemini API integration
- **LLM Integration:** Gemini API (from Google)

### Libraries Used
- `streamlit`
- `google-generativeai` (for Gemini)
- `python-dotenv`
- Standard Python: `json`, `re`, `datetime`, etc.

### File Structure
- `app.py`: Streamlit app logic
- `chatbot.py`: Manages chatbot logic and Gemini interactions
- `config.py`: Stores prompts and API config
- `utils.py`: Helper functions (validation, formatting, etc.)
- `requirements.txt`: All dependencies

---

## Prompt Design

### System Prompt
- Sets the assistant’s personality and task.
- Controls the flow for data collection and assessments.
- Maintains clarity and a professional tone.

### Information Prompts
- Structured prompts to collect name, email, phone, etc.
- Field-specific prompts and validations ensure clean data.

### Technical Assessment Prompts
- Dynamically adapt to the tech stack.
- Cover fundamental to advanced topics.
- Include theoretical and practical questions.

---

## Challenges & Solutions

### 1. Maintaining Context
**Solution:** Used session state to track flow and prevent repeated questions.

### 2. Relevant Question Generation
**Solution:** Engineered prompts using the user’s declared tech stack to personalize questions.

### 3. Invalid Inputs
**Solution:** Added validation checks (e.g., for phone and email formats).

### 4. UI/UX Design
**Solution:** Styled the Streamlit app for better readability and message flow.

### 5. Error Handling
**Solution:** Added exception handling for API failures and logic bugs.

---

## Future Enhancements
- Sentiment analysis for emotion detection
- Support for multilingual interviews
- Custom question difficulty (junior, mid, senior)
- Video/audio input for richer responses
- Candidate analytics dashboard

---

## License
This project is built for educational purposes as part of an AI/ML Intern Assignment for TalentScout recruitment agency.

