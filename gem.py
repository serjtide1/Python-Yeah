import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv('API_KEY'))

# System message to define the persona
kratos_instructions = (
     "You are Kratos from God of War (2018 and Ragnarök). "
    "You speak in a deep, calm, and intimidating tone. "
    "Your responses are short, blunt, and serious. "
    "You rarely joke and never use modern slang. "
    "You often give harsh wisdom and speak with authority. "
    "You may call the user 'Boy' when appropriate. "
    "Stay fully in character at all times."
)

# Initialize the model with system instructions
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=kratos_instructions
)

def start_chat():
    # Start a chat session to maintain context (optional but recommended)
    chat_session = model.start_chat(history=[])
    
    print("I am Kratos Ghost Of Sparta. Speak Boy. (Type 'exit' to leave)")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("We are done here. Do not waste what you have learned.")
            break
        
        try:
            # Send message to the model
            response = chat_session.send_message(user_input)
            print(f"\nKratos: {response.text}\n")
        except Exception as e:
            print(f"An obstacle stands in our way. It will be dealt with: {e}")

if __name__ == "__main__":
    start_chat()
