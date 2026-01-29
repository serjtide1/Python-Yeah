import google.generativeai as genai
import os
import requests
import cv2
from io import BytesIO
from PIL import Image, ImageDraw
from dotenv import load_dotenv
import random

load_dotenv()

print("Using API key:", os.getenv("API_KEY"))
genai.configure(api_key=os.getenv("API_KEY"))

kratos_instructions = (
    "You are Kratos from God of War (2018 and Ragnarök). "
    "You speak in a deep, calm, and intimidating tone. "
    "Your responses are short, blunt, and serious. "
    "You rarely joke and never use modern slang. "
    "You often give harsh wisdom and speak with authority. "
    "You may call the user 'Boy' when appropriate. "
    "You give harsh but meaningful combat wisdom. "
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

def extract_frames(video_path, every_n_seconds=1, max_frames=6):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        raise ValueError("Unable to read video.")
    frame_interval = int(fps * every_n_seconds)
    frames = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            frames.append(pil_image)
            if len(frames) >= max_frames:
                break
        frame_count += 1
    cap.release()
    return frames

def start_chat():
    chat = model.start_chat(history=[])

    print("Kratos stands before you. Speak.")
    print("Commands:")
    print("  image <URL or path>      → Analyze an image")
    print("  video <path>             → Analyze a fighting video")
    print("  weakpoints <URL or path> → Analyze enemy weak points and mark them")
    print("  exit                     → Leave\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Kratos: Go. Do not waste what you have learned.")
            break

        try:
            if user_input.lower().startswith("image "):
                image_source = user_input.split(" ", 1)[1].strip().strip('"')
                image = load_image(image_source)
                response = chat.send_message([
                    "Study this image as a warrior. Judge strength and weakness.",
                    image
                ])
                print(f"\nKratos: {response.text}\n")

            elif user_input.lower().startswith("video "):
                video_path = user_input.split(" ", 1)[1].strip().strip('"')
                frames = extract_frames(video_path)
                if not frames:
                    print("Kratos: There is nothing to analyze.")
                    continue
                response = chat.send_message([
                    "Analyze this combat. Judge technique, mistakes, aggression, and intent.",
                    *frames
                ])
                print(f"\nKratos: {response.text}\n")

            elif user_input.lower().startswith("weakpoints "):
                image_source = user_input.split(" ", 1)[1].strip().strip('"')
                image = load_image(image_source)
                response = chat.send_message([
                    "Study this enemy as a warrior. "
                    "Describe weak points and approximate location visually (e.g., 'left shoulder', 'center chest').",
                    image
                ])
                print(f"\nKratos: {response.text}\n")
                draw = ImageDraw.Draw(image)
                width, height = image.size
                for _ in range(3):
                    x = random.randint(0, width)
                    y = random.randint(0, height)
                    radius = 10
                    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(255,0,0,128))
                output_path = "weakpoints_marked.png"
                image.save(output_path)
                print(f"Weak points marked image saved as {output_path}")

            else:
                response = chat.send_message(user_input)
                print(f"\nKratos: {response.text}\n")

        except Exception as e:
            print("Kratos: An obstacle blocks our path. Control yourself.")
            print(f"Debug: {e}\n")

if __name__ == "__main__":
    start_chat()
