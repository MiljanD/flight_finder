from models.db import Db


class Travels(Db):
    def __init__(self):
        super().__init__()
        self.__location_from = None
        self.__location_from_code = None
        self.__destination = None
        self.__destination_code = None
        self.__travel_date = None
        self.__passengers = None
        self.__desired_price = None
        self.con = self._get_connection()



    @property
    def location_from(self):
        return self.__location_from

    @location_from.setter
    def location_from(self, location):
        if not self.__location_from or not location.strip():
            raise ValueError("Polazna lokacija mora biti uneta.")

        self.__location_from = location


    @property
    def location_from_code(self):
        return self.__location_from_code

    @location_from_code.setter
    def location_from_code(self, location_code):
        if not self.__location_from_code or not location_code.strip():
            raise ValueError("IATA kod aerodroma polazne lokacije mora biti unesen.")

        self.__location_from_code = location_code


    @property
    def destination(self):
        return self.__destination

    @destination.setter
    def destination(self, destination):
        if not self.__destination or not destination.strip():
            raise ValueError("Zeljena destinacija mora biti uneta.")

        self.__destination = destination


    @property
    def destination_code(self):
        return self.__destination_code

    @destination_code.setter
    def destination_code(self, destination_code):
        if not self.__destination_code or not destination_code.strip():
            raise ValueError("Kod aerodroma zeljene destinacije mora biti unesen.")

        self.__destination_code = destination_code


    @property
    def travel_date(self):
        return self.__travel_date

    @travel_date.setter
    def travel_date(self, travel_date):
        if not self.__travel_date or not travel_date.strip():
            raise ValueError("Datum putovanja mora biti unesen.")

        self.__travel_date = travel_date


    @property
    def desired_price(self):
        return self.__desired_price

    @desired_price.setter
    def desired_price(self, price):
        if not self.__desired_price or price <= 0:
            raise ValueError("Zeljena cena mora biti unesena i veca od 0.")

        self.__desired_price = price


    @property
    def passenger_number(self):
        return self.__passengers


    @passenger_number.setter
    def passenger_number(self, passengers):
        if not self.__passengers or passengers <= 0:
            raise ValueError("Broj putnika mora biti unesen i veci od 0.")

        self.__passengers = passengers