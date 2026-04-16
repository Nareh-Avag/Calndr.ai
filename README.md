Hoya Hacks 2026 -calndr.ai
An AI-powered chatbot that builds personalized schedules to help users plan their daily lives more efficiently and maximize productivity.
About
As college students balancing rigorous coursework with other aspects of our lives, managing time efficiently is a constant challenge. Calndr AI was built to act as a personal scheduling assistant — tell it about your day and it'll help you organize your time.
Built With

Python — Backend server handling chat logic and API communication
HTML / CSS / JavaScript — Frontend chat interface
Google Gemini API — Powers the AI conversation and schedule generation

How It Works

Users describe their tasks, deadlines, and availability through a chat interface
The message is sent from the frontend to a Python (Flask) backend
The backend forwards the conversation to the Gemini API, which generates a personalized schedule
The response is streamed back to the chat UI in real time

Getting Started
Prerequisites

Python 3.x
A Google Gemini API key

Installation
bash# Clone the repo
git clone https://github.com/Nareh-Avag/calndr.ai.git
cd calndr.ai

# Install dependencies
pip install flask google-generativeai

# Set your API key
export GEMINI_API_KEY="your-api-key-here"

# Run the backend
python app.py
Then open index.html in your browser (or navigate to http://127.0.0.1:5000).
