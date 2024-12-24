from flask import Flask, request, jsonify
from gemini_chatbot import MedicalChatbot as GeminiChatbot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
chatbot = GeminiChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    # Get data from the request
    data = request.get_json()
    
    message = data.get('message', '')
    name = data.get('memberName')
    dob = data.get('dob') 
    gender = data.get('gender')  
    diseases = data.get('diseases')

    # Calculate age from DOB if necessary
    age = calculate_age(dob) if dob else None

    # Create a member dictionary
    member = {
        'name': name,
        'age': age,
        'gender': gender,
        'diseases': diseases,
        'message': message
    }
    
    # Get the response from the chatbot
    response = chatbot.get_medical_response(member)
    return jsonify(response)

def calculate_age(dob):
    from datetime import datetime
    if dob:
        dob_date = datetime.strptime(dob, '%Y-%m-%dT%H:%M:%S.%fZ')  # Adjust format to match the incoming data
        today = datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        return age
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
