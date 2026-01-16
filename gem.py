import google.generativeai as genai
import os
import requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("API_KEY"))

kratos_instructions = (
    "You are Kratos from God of War (2018 and Ragnarök). "
    "You speak in a deep, calm, and intimidating tone. "
    "Your responses are short, blunt, and serious. "
    "You rarely joke and never use modern slang. "
    "You often give harsh wisdom and speak with authority. "
    "You may call the user 'Boy' when appropriate. "
    "Stay fully in character at all times."
)

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=kratos_instructions
)


def load_image(source):
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    else:
        return Image.open(source)

def start_chat():
    chat = model.start_chat(history=[])
    print("I am Kratos. Speak, Boy. (Type 'exit' to leave)")
    print("To analyze an image, type: image <URL or local path>")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("We are done here. Do not waste what you have learned.")
            break

        try:
            if user_input.lower().startswith("image "):
                image_source = user_input.split(" ", 1)[1].strip().strip('"')
                image = load_image(image_source)

                response = chat.send_message([
                    "Study this image as a warrior would. Speak truth.",
                    image
                ])
            else:
                response = chat.send_message(user_input)

            print(f"\nKratos: {response.text}\n")

        except Exception as e:
            print(f"Kratos: An obstacle blocks our path. {e}")

if __name__ == "__main__":
    start_chat()
