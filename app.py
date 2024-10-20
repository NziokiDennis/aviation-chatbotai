# app.py

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Route for rendering the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling user input and sending it to the chatbot
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message")

    if user_message:
        rasa_url = "http://localhost:5005/webhooks/rest/webhook"
        headers = {'Content-Type': 'application/json'}
        payload = {"sender": "user", "message": user_message}

        try:
            response = requests.post(rasa_url, headers=headers, json=payload)
            bot_responses = response.json()

            # Check if bot responses are valid and have messages
            if bot_responses and isinstance(bot_responses, list):
                return jsonify({"response": bot_responses[0].get('text', "I couldn't find relevant information.")})
            else:
                return jsonify({"response": "I couldn't find relevant information."})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"response": "Error occurred while connecting to the bot."})

    return jsonify({"response": "No message received."})

if __name__ == '__main__':
    app.run(debug=True)
