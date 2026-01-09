from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_AI_API_KEY"),
    http_options={"api_version": "v1"}  # 🔥 FORCE v1
)

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Say hello"
)

print(response.text)
