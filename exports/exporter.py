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
        try:
            query = "SELECT * FROM tokens WHERE status=%s ORDER BY created_at LIMIT 1"
            return self._execute_query(query, ("active",))
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri ekstrakciji podataka: {e}")


    def export_travel_details(self):
        try:
            query = "SELECT * FROM travel_details"
            return self._execute_query(query)
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri ekstrakciji podataka: {e}")
