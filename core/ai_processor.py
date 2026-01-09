import os
import json
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class AIProcessor:
    def __init__(self):
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_AI_API_KEY missing in .env")
        
        # Configure the library
        genai.configure(api_key=api_key)
        
        # Flash model handwriting/tables ke liye best hai
        self.model = genai.GenerativeModel('models/gemini-3-flash-preview')

    def process_handwriting_to_json(self, image_path):
        try:
            if not os.path.exists(image_path):
                print(f"File not found: {image_path}")
                return None
                
            raw_image = Image.open(image_path)
            
            # Form ke columns ke hisaab se specific prompt
            prompt = """
            Analyze this image and identify the table. 
            1. Detect all column headers present in the table.
            2. Extract all rows into a JSON array of objects.
            3. Use the detected headers as keys for the JSON objects.
            4. If a cell is empty, use "".
            
            Return ONLY the raw JSON array. No markdown, no conversational text.
            """

            # Correct method for this library
            response = self.model.generate_content([prompt, raw_image])
            
            if response and response.text:
                text = response.text.strip()
                # Remove markdown if present
                if '```' in text:
                    text = text.replace('```json', '').replace('```', '').strip()
                
                return json.loads(text)
            
            return None
            
        except Exception as e:
            print(f"Gemini Error: {str(e)}")
            return None