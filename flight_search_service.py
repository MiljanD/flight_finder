import requests
from token_manager import TokenManager
from models.db import Db
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class FlightSearchService(Db):
    flight_service_endpoint = os.getenv("FLIGHT_SERVICE_ENDPOINT")
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.token = TokenManager()
        self.location_code = None
        self.destination_code = None
        self.departure_date = None
        self.passengers = None


    def get_flights(self):
        valid_token = self.token.get_valid_token()

        params = {
            f"originLocationCode": {self.location_code},
            "destinationLocationCode": {self.destination_code},
            "departureDate": {self.departure_date},
            "adults": {self.passengers},
            "max": 2
        }

        headers = {
            "Authorization": f"Bearer {valid_token}"
        }

        response = requests.get(url=self.flight_service_endpoint, params=params, headers=headers)

        print(response.json())


