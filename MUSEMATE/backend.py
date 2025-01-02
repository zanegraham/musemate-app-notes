from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("musemate-app-firebase-adminsdk-2wehe-e8d7e3991f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Flask app
app = Flask(__name__)

# Mistral API setup
mistral_api_key = "VL3iGfJYVp1jitUth4ZHlhgBHGL33Nu4"

# Route to save ideas to Firebase Firestore
@app.route('/save_idea', methods=['POST'])
def save_idea():
    idea_text = request.json.get("idea", "")
    if not idea_text:
        return jsonify({"error": "Idea cannot be empty"}), 400

    # Save idea to Firestore with timestamp
    idea_data = {
        "idea": idea_text,
        "timestamp": datetime.now()
    }
    db.collection('ideas').add(idea_data)
    return jsonify({"status": "Idea saved successfully!"})

# Route to interact with Mistral AI
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Send the user input to Mistral API for response
    headers = {
        "Authorization": f"Bearer {mistral_api_key}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": user_input}
    response = requests.post("https://api.mistral.ai/chat", headers=headers, json=payload)
    ai_reply = response.json().get("response", "No response")
    return jsonify({"reply": ai_reply})

if __name__ == '__main__':
    app.run(debug=True)
