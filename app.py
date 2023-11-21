import streamlit as st
import pandas as pd
import requests

# Function to search flights using Gol Smiles API
def search_flights(origin, destination, departure_date, end_date):
    # Replace this with actual API request to Gol Smiles
    # For demonstration purposes, just returning a DataFrame
    data = {
        'Flight Number': ['SM123', 'SM456', 'SM789'],
        'Origin': [origin, origin, origin],
        'Destination': [destination, destination, destination],
        'Departure Date': [departure_date, departure_date, departure_date],
        'End Date': [end_date, end_date, end_date],
        'Duration': ['2h', '3h', '4h'],
        'Price': ['$200', '$300', '$400']
    }
    return pd.DataFrame(data)

# Streamlit app
st.set_page_config(page_title="Buscador Smiles", page_icon=":airplane:")

# Header
st.title("Buscador Smiles")

# Form for flight search
with st.form("flight_search_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        origin = st.text_input("Origen", "BUE")

    with col2:
        destination = st.text_input("Destino", "BCN")

    with col3:
        departure_date = st.date_input("Desde", pd.to_datetime("today"))
        end_date = st.date_input("Hasta", pd.to_datetime("today"))

    search_button = st.form_submit_button("Buscar Vuelos")

# Display search results
if search_button:
    st.subheader("Resultados de la búsqueda")

    # Make API request
    api_url = "https://api-airlines-boarding-tax-prd.smiles.com.br/v1/airlines/flight/boardingtax"
    params = {
        "from": origin,
        "to": destination,
        "adults": 1,
        "children": 0,
        "infants": 0,
        "fareuid": "976de4a275",
        "uid": "d9268438a66bde0382be",
        "type": "SEGMENT_1",
        "highlightText": "SMILES_CLUB",
    }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        # Parse the API response and display results
        flights_df = search_flights(origin, destination, departure_date, end_date)
        st.write(flights_df)
    else:
        st.error(f"Error connecting to Gol Smiles API. Status code: {response.status_code}")
