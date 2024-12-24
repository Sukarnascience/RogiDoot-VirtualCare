from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests

preLoadData = """You are a medical diagnostic assistant. Provide a diagnosis and recommendations based on the following input.
Format your response as follows:
- Name: [Patient's Name]
- Age: [Patient's Age]
- Assumed Issues: [List of possible issues]
- Most Common Solution: [Suggested solution]
- If Required, Recommended Medication: [List of medications]
- Contact: [Which doctor to meet: Cardiology/Orthopedics/...etc.] (Sujest the doctor which is rewuired for this treatment)"""

class MedicalChatbot:
    def __init__(self):
        print("""Hi! This is BeeBotix, the creator of this code.
Just a friendly reminder to create a .env file and set your GOOGLE_API_KEY environment variable before using this program.
Thank you!
================= Happy Chatting =================""")
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            print("Invalid/No API Key in .env file")
            return

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat(history=[])

    def check_internet_connection(self):
        try:
            requests.get("https://www.google.com", timeout=1)
            return True
        except requests.ConnectionError:
            return False

    def get_medical_response(self, member):
        name = member.get('name')
        age = member.get('age')
        gender = member.get('gender')
        diseases = member.get('diseases')
        message = member.get('message')

        question = f"where the given data of Patient are> Name: {name}, Age: {age}, Gender: {gender}, Diseases: {diseases}, Message: {message}"
        full_prompt = preLoadData + "\n" + question
        print(full_prompt)

        if not self.check_internet_connection():
            return {"message": "Sorry, can't connect to the internet. Please check your connection."}

        response = self.chat.send_message(full_prompt, stream=True)

        # Check the safety ratings
        for chunk in response:
            if hasattr(chunk, 'safety_ratings'):
                print(f"Safety Ratings: {chunk.safety_ratings}")  # Log safety ratings
            if hasattr(chunk, 'text'):
                return {"message": " ".join(chunk.text for chunk in response)}

        return {"message": "No valid response received from the AI model."}


'''
# Example usage
if __name__ == "__main__":
    chatbot = MedicalChatbot()
    # Simulate a request from the frontend
    sample_member = {
        'name': "John Doe",
        'age': 30,
        'gender': "Male",
        'diseases': "hypertension, diabetes",
        'message': "I've been feeling dizzy lately."
    }
    response = chatbot.get_medical_response(sample_member)
    print(response)
'''