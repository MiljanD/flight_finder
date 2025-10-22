import requests
from token_generator.token_manager import TokenManager
from exports.exporter import Exporter
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class FlightSearchService:
    """
    Class is responsible for collecting flights data from Amadeus API service.
    Returns collected data for further actions.
    """
    flight_service_endpoint = os.getenv("FLIGHT_SERVICE_ENDPOINT")
    def __init__(self):
        self.token = TokenManager()
        self.exports = Exporter()
        self.location_code = None
        self.destination_code = None
        self.departure_date = None
        self.passengers = None
        self.price_limit = None


    def get_flights(self) -> dict:
        """
        Sends request to Amadeus API service based on provided parameters.
        :return: Collected data in a form of dict.
        """
        valid_token = self.token.get_valid_token()

        params = {
            "originLocationCode": self.location_code,
            "destinationLocationCode": self.destination_code,
            "departureDate": self.departure_date,
            "adults": self.passengers,
            "maxPrice": self.price_limit
        }

        headers = {
            "Authorization": f"Bearer {valid_token}"
        }

        response = requests.get(url=self.flight_service_endpoint, params=params, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(f"Greska prilikom skupljanja podataka: {response.status_code} - {response.text}")

        try:
            return response.json()
        except ValueError:
            raise RuntimeError("Nevalidan JSON odgovor od API servisa.")


    def reset_travel_data(self) -> None:
        """
        Resets values of instance attributes to default values.
        """
        self.location_code = None
        self.destination_code = None
        self.departure_date = None
        self.passengers = None
        self.price_limit = None


    def flight_details_collection(self) -> list:
        """
        Generates instance attributes that will be used as parameters of API call.
        :return: Collected data in form of list of dicts
        """
        flight_details = self.exports.export_travel_details()
        if not flight_details:
            return []

        collected_data = []
        for flight in flight_details:
            self.location_code = flight["location_code"]
            self.destination_code = flight["destination_code"]
            self.departure_date = flight["travel_date"]
            self.passengers = flight["passengers"]
            self.price_limit = flight["desired_price"]

            collected_data.append(self.get_flights())
            self.reset_travel_data()

        return collected_data
