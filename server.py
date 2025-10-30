from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Replace with your real API key if using Google Maps
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

def get_route(source, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={source}&destination={destination}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        route_steps = []
        for step in data["routes"][0]["legs"][0]["steps"]:
            route_steps.append(step["html_instructions"])  # Step-by-step directions
        
        return " ➝ ".join(route_steps)  # Combine steps with an arrow
    else:
        return "Sorry, I couldn't find a route. Please try again."

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").lower()

    if "route" in user_message or "travel" in user_message:
        words = user_message.split()
        if "from" in words and "to" in words:
            source = words[words.index("from") + 1]
            destination = words[words.index("to") + 1]
            route_info = get_route(source, destination)
            return jsonify({"response": f"Here is the best route from {source} to {destination}: {route_info}"})

    return jsonify({"response": f"You said: {user_message}. I will help you with travel-related queries soon!"})

if __name__ == "__main__":
    app.run(debug=True)
