import pymysql


class Db:
    def __init__(self):
        self.__connection = None


    def _get_connection(self):
        if self.__connection is None:
            try:
                self.__connection = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="dm3004^mk2606",
                    database="flight_finder",
                    cursorclass=pymysql.cursors.DictCursor
                )
            except pymysql.MySQLError as e:
                raise RuntimeError(f"Neuspesna konekcija ka bazi: {e}")

        return self.__connection


    def close_connection(self):
        if self.__connection:
            self.__connection.close()
            self.__connection = None