import requests

# Your API key
API_KEY = '43c91e029cd476e5a13591e6e75d7b43'

# Base URL for AviationStack API
BASE_URL = 'http://api.aviationstack.com/v1/flights'

def get_flight_info(flight_number):
    # Prepare the API request URL with flight number
    params = {
        'access_key': API_KEY,
        'flight_iata': flight_number  # Using IATA flight code
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

# Prompt for a flight number
flight_number = input("Please enter your flight number: ")

# Fetch the flight info
flight_info = get_flight_info(flight_number)

if flight_info:
    flight_status = flight_info['flight_status']
    airline_name = flight_info['airline']['name']
    departure_airport = flight_info['departure']['airport']
    departure_gate = flight_info['departure']['gate']
    departure_time = flight_info['departure']['scheduled']
    arrival_airport = flight_info['arrival']['airport']
    arrival_time = flight_info['arrival']['scheduled']

    # Display the flight details
    print(f"\nFlight {flight_number} status: {flight_status}")
    print(f"Airline: {airline_name}")
    print(f"Departure: {departure_airport}, Gate: {departure_gate}, Scheduled: {departure_time}")
    print(f"Arrival: {arrival_airport}, Scheduled: {arrival_time}")
else:
    print(f"Flight {flight_number} not found. Please check the flight number and try again.")
