import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. Create a .env file with your API key.")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# System prompt that defines the chatbot's personality and expertise
SYSTEM_PROMPT = """You are an expert time management coach for college students. Your role is to:
- Help students organize their schedules and prioritize tasks
- Suggest study techniques (Pomodoro method , time blocking, etc.)
- Create realistic timelines for assignments and exams
- Help reduce procrastination and stress
- Offer advice on balancing academics, extracurriculars, and self-care

Be friendly, supportive, and practical. Keep responses concise and actionable."""

def chat_with_bot(conversation_history):
    """Send conversation history to Gemini and get response."""
    response = model.generate_content(conversation_history)
    return response.text

def main():
    """Main chatbot loop."""
    print("=" * 60)
    print("calndr.ai")
    print("=" * 60)
    print("Hi! I'm calndr.ai. to start, please tell me your schedule")
    print("managing your schedule, studying, or organizing your tasks!")
    print("Type 'exit' to quit.\n")
    
    conversation_history = [
        genai.protos.Content(
            role="user",
            parts=[genai.protos.Part(text=SYSTEM_PROMPT)]
        ),
        genai.protos.Content(
            role="model",
            parts=[genai.protos.Part(text="I understand. I'm here to help college students manage their time effectively.")]
        )
    ]
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("Bot: Good luck with your studies! You've got this! 💪")
            break
        
        if not user_input:
            continue
        
        # Add user message to history
        conversation_history.append(
            genai.protos.Content(
                role="user",
                parts=[genai.protos.Part(text=user_input)]
            )
        )
        
        # Get bot response
        bot_response = chat_with_bot(conversation_history)
        
        # Add bot response to history
        conversation_history.append(
            genai.protos.Content(
                role="model",
                parts=[genai.protos.Part(text=bot_response)]
            )
        )
        
        print(f"\nBot: {bot_response}\n")

if __name__ == "__main__":
    main()




