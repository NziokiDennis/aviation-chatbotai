from rasa_sdk import Action
import requests

API_KEY = '43c91e029cd476e5a13591e6e75d7b43'
BASE_URL = 'http://api.aviationstack.com/v1/flights'

class ActionFlightStatus(Action):
    def name(self):
        return "action_flight_status"

    def run(self, dispatcher, tracker, domain):
        # Retrieve the flight number from the slot
        flight_number = tracker.get_slot('flight_number')

        if not flight_number:
            dispatcher.utter_message(text="Could you please provide a flight number?")
            return []

        # Call the API to get flight status
        flight_info = get_flight_info(flight_number)

        if flight_info:
            flight_status = flight_info['flight_status']
            airline_name = flight_info['airline']['name'] if flight_info['airline'] else "Unknown"
            departure_airport = flight_info['departure']['airport'] if flight_info['departure'] else "Unknown"
            departure_gate = flight_info['departure']['gate'] if flight_info['departure'] and flight_info['departure']['gate'] else "N/A"
            departure_time = flight_info['departure']['scheduled'] if flight_info['departure'] else "Unknown"
            arrival_airport = flight_info['arrival']['airport'] if flight_info['arrival'] else "Unknown"
            arrival_time = flight_info['arrival']['scheduled'] if flight_info['arrival'] else "Unknown"

            # Formulate the response using the new response template
            response_text = (
                f"Sure! The status of flight {flight_number} is currently {flight_status}. "
                f"Airline: {airline_name}. "
                f"Departure: {departure_airport}, Gate: {departure_gate}, Scheduled: {departure_time}. "
                f"Arrival: {arrival_airport}, Scheduled: {arrival_time}. Let me know if you need anything else!"
            )

            # Send the formatted response back to the user
            dispatcher.utter_message(text=response_text)

            # Reset relevant slots after responding
            tracker.slots['flight_number'] = None  # Clear flight number slot
            tracker.slots['departure_gate'] = None
            tracker.slots['flight_status'] = None
            tracker.slots['airline_name'] = None
            tracker.slots['departure_airport'] = None
            tracker.slots['departure_time'] = None
            tracker.slots['arrival_airport'] = None
            tracker.slots['arrival_time'] = None
        else:
            # Handle case where flight information is not found
            dispatcher.utter_message(text=f"I'm sorry, but I couldn't find any information for flight {flight_number}. Please check the flight number and try again.")

        return []

def get_flight_info(flight_number):
    # Prepare the API request URL with flight number
    params = {
        'access_key': API_KEY,
        'flight_iata': flight_number.strip().replace(" ", "")  # Normalize the flight number by removing spaces
    }

    # Make the API request
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'data' in data and len(data['data']) > 0:
            return data['data'][0]  # Return the first flight result
        else:
            return None
    else:
        return None

class ActionGateInfo(Action):
    def name(self):
        return "utter_gate_info"

    def run(self, dispatcher, tracker, domain):
        departure_gate = tracker.get_slot('departure_gate')
        if departure_gate:
            dispatcher.utter_message(text=f"The departure gate for your flight is {departure_gate}.")
        else:
            dispatcher.utter_message(text="I don't have gate information available at the moment.")

        return []
