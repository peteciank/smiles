import json
import requests
import streamlit as st
import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Constants
date_layout = "%Y-%m-%d"
big_max_miles_number = 9_999_999

# Gol Smiles API URL
api_url = "https://api-air-flightsearch-prd.smiles.com.br/v1/airlines/search"

# Gol Smiles API Key and Headers
api_key = "aJqPU7xNHl9qN3NVZnPaJ208aPo2Bh2p2ZV844tw"
headers = {
    "x-api-key": api_key,
    "region": "ARGENTINA",
    "origin": "https://www.smiles.com.ar",
    "referer": "https://www.smiles.com.ar",
    "channel": "web",
}

# Function to create a URL for flight search
def create_url(departure_date, origin_airport, destination_airport):
    params = {
        "departureDate": departure_date,
        "originAirportCode": origin_airport,
        "destinationAirportCode": destination_airport,
        "adults": 1,
        "cabinType": "all",
        "children": 0,
        "currencyCode": "ARS",
        "infants": 0,
        "isFlexibleDateChecked": False,
        "tripType": 2,
        "forceCongener": True,
        "r": "ar",
    }
    return api_url + "?" + "&".join(f"{key}={value}" for key, value in params.items())

# Function to make an API request
def make_request(departure_date, origin_airport, destination_airport):
    url = create_url(departure_date, origin_airport, destination_airport)
    response = requests.get(url, headers=headers)
    return response.content

# Function to parse JSON response
def parse_response(response):
    return json.loads(response)

# Function to process flight results
def process_results(results):
    # Implement your logic to process the flight results
    pass

# Function to perform a flight search for a specific date range
def perform_flight_search(starting_departure_date, starting_returning_date, origin_airport, destination_airport, days_to_query):
    departure_dates = [starting_departure_date + datetime.timedelta(days=i) for i in range(days_to_query)]

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for departure_date in departure_dates:
            futures.append(
                executor.submit(make_request, departure_date.strftime(date_layout), origin_airport, destination_airport)
            )

        results = [future.result() for future in tqdm(futures, desc="Fetching flight data", unit="request")]

    parsed_results = [parse_response(result) for result in results]
    process_results(parsed_results)

# Streamlit app
st.title("Gol Smiles Flight Search")

# Input widgets for user parameters
origin_airport = st.text_input("Enter Origin Airport Code:")
destination_airport = st.text_input("Enter Destination Airport Code:")
departure_date = st.date_input("Select Departure Date:")
return_date = st.date_input("Select Return Date:")
days_to_query = st.slider("Select Number of Days to Query", min_value=1, max_value=10, value=5)

# Button to trigger the flight search
if st.button("Search Flights"):
    starting_departure_date = datetime.datetime(departure_date.year, departure_date.month, departure_date.day)
    starting_returning_date = datetime.datetime(return_date.year, return_date.month, return_date.day)

    perform_flight_search(
        starting_departure_date, starting_returning_date, origin_airport, destination_airport, days_to_query
    )
