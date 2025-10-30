from models.db import Db
import pymysql


class Exporter(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()


    def _execute_query(self, query, params=None):
        try:
            with self.con.cursor() as cursor:
                cursor.execute(query, params or ())
                self.con.commit()
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri ekstrakciji podataka: {e}")


    def get_all_tokens(self):
        query = "SELECT * FROM tokens"
        return self._execute_query(query)


    def valid_token(self):
        query = "SELECT * FROM tokens WHERE status=%s ORDER BY created_at LIMIT 1"
        return self._execute_query(query, ("active",))


    def export_travel_details(self):
        query = "SELECT * FROM travel_details"
        return self._execute_query(query)



    def export_last_added_flight_id(self):
        query = "SELECT id FROM flights ORDER BY id DESC LIMIT 1"
        return self._execute_query(query)


    def export_date_and_id(self):
        query = "SELECT id, travel_date FROM travel_details"
        return self._execute_query(query)



    def is_cheaper_than_existing(self, travel_id):
        query = "SELECT price FROM flights WHERE travel_id=%s ORDER BY price ASC LIMIT 1"
        return self._execute_query(query, (travel_id, ))


    def are_stored_flights(self, travel_id):
        query = "SELECT id FROM flights WHERE travel_id=%s"
        return self._execute_query(query, (travel_id, ))


    def get_table_columns(self, table_name) -> list[str]:
        query = f"SHOW COLUMNS FROM {table_name}"
        return self._execute_query(query)


    def id_exists(self, table_name, identifier) -> bool:
        query = f"SELECT id FROM {table_name} WHERE id=%s"
        result = self._execute_query(query, (identifier, ))
        return bool(result)


    def export_complete_flights_data(self):
        query = ("SELECT "
                 "td.location AS 'Polazna Lokacija', td.destination AS 'Odrediste',"
                 "td.travel_date AS 'Datum polaska', td.passengers AS 'Broj putnika', "
                 "f.departure_time AS 'Vreme polaska', f.departure_terminal AS 'Terminal polaska', "
                 "f.arrival_time AS 'Vreme pristizanja', f.arrival_terminal AS 'Terminal pristizanja', f.price AS 'Cena',"
                 "t.transfer_airport AS 'Aerodrom transfer', t.arrival_time AS 'Vreme stizanja na transfer', "
                 "t.departure_time AS 'Vreme polaska sa transfera' "
                 "FROM travel_details td "
                 "LEFT JOIN flights f ON f.travel_id = td.id "
                 "LEFT JOIN transfers t ON t.flight_id = f.id "
                 "ORDER BY td.id")

        return self._execute_query(query)




if __name__ == "__main__":
    export = Exporter()
    print(export.export_complete_flights_data())
