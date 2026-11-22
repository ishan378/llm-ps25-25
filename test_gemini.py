
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Sending request to Gemini...")

response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Create a 2-day study plan for Java. Keep it short."
)

print("\nGemini Response:")
print(response.output_text)

print("\nGemini test completed!")
