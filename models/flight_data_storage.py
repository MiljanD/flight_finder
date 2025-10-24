from flight_collections.flight_data_parser import FlightDataParser
from models.db import Db


class FlightDataStorage(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.flights = FlightDataParser()


    def flight_data_preparation(self):
        flights = self.flights.parse_flight_data()

        for flight in flights:
            travel_id = flight["travel_id"]
            departure_time = flight["departure"]["at"]
            departure_terminal = flight["departure"]["terminal"]
            flight_price = float(flight["price"])
            arrival_time = None
            arrival_terminal = None
            transfer_airport = None
            arrival_at_transfer_airport = None
            departure_from_transfer_airport = None

            if not flight["transfers"]:
                arrival_time = flight["arrival"]["at"]
                arrival_terminal = flight["arrival"]["terminal"]
            else:
                transfers = flight["transfers"]
                arrival_time = transfers[-1]["arrival"]["at"]
                arrival_terminal = transfers[-1]["arrival"]["terminal"]
                arrival_at_transfer_airport = flight["arrival"]["at"]
                for transfer in transfers:
                    transfer_airport = transfer["departure"]["iataCode"]
                    departure_from_transfer_airport = transfer["departure"]["at"]

            print(travel_id, departure_time, departure_terminal, arrival_terminal, arrival_time,
                  flight_price, transfer_airport, departure_from_transfer_airport, arrival_at_transfer_airport)







if __name__ == "__main__":
    data_storage = FlightDataStorage()
    data_storage.flight_data_preparation()