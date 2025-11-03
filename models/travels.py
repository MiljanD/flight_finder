import pymysql
from exports.exporter import Exporter
from models.db import Db
from utils.date_converter import DateConverter


class Travels(Db):
    """
    Responsible for handling travel details via CRUD operations.
    """
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
        self.exports = Exporter()
        self.converter = DateConverter()



    @property
    def location_from(self) -> str:
        """
        Gets the name of the departure location entered by the user.
        :return:  Capitalized name of the departure location.
        """
        return self.__location_from

    @location_from.setter
    def location_from(self, location):
        """
        Sets the capitalized name of the departure location entered by the user.
        :param location:  Location of departure entered by user.
        """
        if not location.strip():
            raise ValueError("Polazna lokacija mora biti uneta.")

        self.__location_from = location.strip().capitalize()


    @property
    def location_from_code(self) -> str:
        """
        Gets the IATA code of the departure airport entered by the user.
        :return: IATA code of departure airport.
        """
        return self.__location_from_code

    @location_from_code.setter
    def location_from_code(self, location_code):
        """
        Sets the upper case form of IATA code of the departure airport entered by the user.
        :param location_code: Departure airport IATA code.
        :return:
        """
        if not location_code.strip():
            raise ValueError("IATA kod aerodroma polazne lokacije mora biti unesen.")

        self.__location_from_code = location_code.strip().upper()


    @property
    def destination(self) -> str:
        """
        Gets the name of the destination entered by the user.
        :return: Capitalized name of the destination.
        """
        return self.__destination

    @destination.setter
    def destination(self, destination):
        """
        Sets the capitalized name of the destination entered by the user.
        :param destination: Location of destination entered by user.
        """
        if not destination.strip():
            raise ValueError("Zeljena destinacija mora biti uneta.")

        self.__destination = destination.strip().capitalize()


    @property
    def destination_code(self) -> str:
        """
        Gets the IATA code of the destination airport entered by the user.
        :return: Destination airport IATA code.
        """
        return self.__destination_code

    @destination_code.setter
    def destination_code(self, destination_code):
        """
        Sets the upper case form of IATA code of the destination airport entered by the user.
        :param destination_code: Destination airport IATA code.
        """
        if not destination_code.strip():
            raise ValueError("Kod aerodroma zeljene destinacije mora biti unesen.")

        self.__destination_code = destination_code.strip().upper()


    @property
    def travel_date(self) -> str:
        """
        Gets date of specific travel.
        :return: Travel date.
        """
        return self.__travel_date

    @travel_date.setter
    def travel_date(self, travel_date):
        """
        Sets date for specific travel.
        :param travel_date: Desired date for specific travel.
        """
        if not travel_date.strip():
            raise ValueError("Datum putovanja mora biti unesen.")

        self.__travel_date = travel_date.strip()


    @property
    def desired_price(self) -> int:
        """
        Gets desired price limit for specific travel.
        :return: Price limit.
        """
        return self.__desired_price

    @desired_price.setter
    def desired_price(self, price):
        """
        Sets desired price limit for specific travel.
        :param price: Price limit entered by user.
        """
        if not price or int(price) <= 0:
            raise ValueError("Zeljena cena mora biti unesena i veca od 0.")

        self.__desired_price = int(price)


    @property
    def passenger_number(self) -> int:
        """
        Gets the number of passengers for specific travel.
        :return: Number of passengers
        """
        return self.__passengers


    @passenger_number.setter
    def passenger_number(self, passengers):
        """
        Sets number of passengers for specific travel.
        :param passengers: Number of passengers entered by user.
        """
        if not passengers or int(passengers) <= 0:
            raise ValueError("Broj putnika mora biti unesen i veci od 0.")

        self.__passengers = int(passengers)


    def _execute_query(self, query, params) -> None:
        """
        Executes a parameterized SQL query to store data in database.
        :param query: Query that will be executed.
        :param params: Necessary parameters for  executing query.
        """
        with self.con.cursor() as cursor:
            try:
                cursor.execute(query, params)
                self.con.commit()
            except pymysql.MySQLError() as e:
                raise RuntimeError(f"Greska pri CRUD operacijama: {e}")


    def store_travel_details(self) -> None:
        """
        Stores travel details entered by user into database
        """
        query = ("INSERT INTO travel_details "
                 "(location, location_code, destination, destination_code, travel_date, passengers, desired_price)"
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                 )
        params = (self.__location_from, self.__location_from_code,
                  self.__destination, self.__destination_code, self.__travel_date,
                  self.__passengers, self.__desired_price)

        self._execute_query(query, params)


    def delete_passed_travel_details(self) -> None:
        """
        Maintaining fulfillment of travel_details table.
        """
        exported_dates = self.exports.export_date_and_id()
        query = "DELETE FROM travel_details WHERE id=%s"

        for date in exported_dates:
            # Removes records from travel_details table where travel date is passed.
            if self.converter.is_passed_date(date["travel_date"]):
                self._execute_query(query, (date["id"]))


    def delete_travel_details(self, travel_id):
        """
        Removes travel record by ID.
        :param travel_id: Travel record ID.
        """
        if not self.exports.id_exists("travel_details", travel_id):
            raise ValueError("ID putovanja ne  postoji u tabeli.")

        query = "DELETE FROM travel_details WHERE id=%s"
        self._execute_query(query, (travel_id, ))


    def update_travel_details(self, travel_id, column_name, new_value) -> None:
        """
        Enables updating travel_details table data.
        :param travel_id: Travel record ID.
        :param column_name: Name of column that will be updated.
        :param new_value: New value that will be entered into database table.
        """
        valid_columns = self.exports.get_table_columns("travel_details")
        if column_name not in valid_columns:
            raise ValueError("Nepoznata kolona.")

        if not self.exports.id_exists("travel_details", travel_id):
            raise ValueError("ID putovanja ne  postoji u tabeli.")

        query = f"UPDATE travel_details SET {column_name}=%s WHERE id=%s"
        self._execute_query(query, (new_value, travel_id))
