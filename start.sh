#!/bin/bash
# Start the action server
rasa run actions &

# Train the model if not trained
rasa train

# Start the Rasa server with API enabled
rasa run --enable-api --cors "*" --port 5005 &

# Start the Flask app
python app.py
