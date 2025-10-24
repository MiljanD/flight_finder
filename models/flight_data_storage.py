import pymysql
from flight_collections.flight_data_parser import FlightDataParser
from exports.exporter import Exporter
from models.db import Db


class FlightDataStorage(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.flights = FlightDataParser()
        self.exports = Exporter()


    def _execute_storing_query(self, query, params):
        try:
            with self.con.cursor() as cursor:
                cursor.execute(query, params)
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri ekstrakciji podataka: {e}")


    def store_flight_data(self, flight_params):
        query = ("INSERT INTO flights "
                 "(travel_id, departure_time, departure_terminal, arrival_time, arrival_terminal, price) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        params = flight_params
        self._execute_storing_query(query, params)


    def store_transfer_data(self, transfer_params):
        query = ("INSERT INTO transfers"
                 "(flight_id, transfer_airport, arrival_time, departure_time)"
                 "VALUES (%s, %s, %s, %s)")
        params = transfer_params
        self._execute_storing_query(query, params)


    def flight_data_storage(self):
        flights = self.flights.parse_flight_data()
        comparison_travel_id = None
        lowest_stored_price = None

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

            if comparison_travel_id is None or travel_id != comparison_travel_id:
                comparison_travel_id = travel_id
                if self.exports.are_stored_flights(travel_id):
                    result = self.exports.is_cheaper_than_existing(travel_id)
                    lowest_stored_price = result[0]["price"] if result else None


            if lowest_stored_price is None or lowest_stored_price > flight_price:
                if not flight["transfers"]:
                    arrival_time = flight["arrival"]["at"]
                    arrival_terminal = flight["arrival"]["terminal"]
                    flight_parameters = (travel_id, departure_time, departure_terminal, arrival_time, arrival_terminal,
                                         flight_price)
                    self.store_flight_data(flight_parameters)
                else:
                    transfers = flight["transfers"]
                    arrival_time = transfers[-1]["arrival"]["at"]
                    arrival_terminal = transfers[-1]["arrival"]["terminal"]
                    flight_parameters = (travel_id, departure_time, departure_terminal, arrival_time, arrival_terminal,
                                         flight_price)
                    self.store_flight_data(flight_parameters)
                    arrival_at_transfer_airport = flight["arrival"]["at"]

                    flight_id = self.exports.export_last_added_flight_id()[0]["id"]

                    for transfer in transfers:
                        transfer_airport = transfer["departure"]["iataCode"]
                        departure_from_transfer_airport = transfer["departure"]["at"]

                        transfer_parameters = (flight_id, transfer_airport, arrival_at_transfer_airport,
                                               departure_from_transfer_airport)
                        self.store_transfer_data(transfer_parameters)
