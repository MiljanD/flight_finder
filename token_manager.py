from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime, timedelta
import requests
from models.db import Db
from exports.exporter import Exporter

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class TokenManager(Db):
    """
    Class for managing necessary auth token for Amadeus API service.
    Inherits from Db for database access.
    Enables generation and storing new auth token if active token is not available in database.
    """

    # class variables necessary for granting the access to  Amadeus API service
    token_endpoint = os.getenv("TOKEN_ENDPOINT")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.token = None
        self.generated_at = None
        self.expires = None
        self.exports = Exporter()


    def generate_token(self) -> None:
        """
        Uses Amadeus API service to generate new token.
        Generated data are parsed and prepared as instance attributes for storing in database
        """
        parameters = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }

        headers = {
            "Content-type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url=self.token_endpoint, data=parameters, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Greska prilikom generisanja tokena: {response.status_code} - {response.text}")

        token_data = response.json()

        self.token = token_data["access_token"]
        self.generated_at = datetime.now()
        self.expires = datetime.now() + timedelta(seconds=token_data["expires_in"] - 60)


    def reset_token_data(self) -> None:
        """
        Resets values of instance attributes to default values.
        """
        self.token = None
        self.generated_at = None
        self.expires = None


    def store_token(self) -> None:
        """
        Method for storing token data to database.
        """
        with self.con.cursor() as cursor:
            query = ("INSERT INTO tokens (token, created_at, expire, status) "
                     "VALUES (%s, %s, %s, %s)")
            cursor.execute(query, (self.token, self.generated_at, self.expires, "active"))
            self.con.commit()

        self.reset_token_data()


    def update_token_status(self) -> None:
        """
        Responsible for keeping token status updated.
        """
        all_tokens = self.exports.get_all_tokens()
        for current_token in all_tokens:
            if current_token["expire"] < datetime.now() and current_token["status"] != "inactive":
                with self.con.cursor() as cursor:
                    query = "UPDATE tokens SET status=%s WHERE id=%s"
                    cursor.execute(query, ("inactive", current_token["id"]))
                    self.con.commit()



    def get_valid_token(self) -> str:
        """
        Responsible for keeping token data updated and providing active token to next service.
        :return: Active auth token for Amadeus API service.
        """
        self.update_token_status()
        active_token = self.exports.valid_token()
        if (
            isinstance(active_token, list)
            and active_token
            and isinstance(active_token[0], dict)
            and "token" in active_token[0]
        ):
            return active_token[0]["token"]

        self.generate_token()
        new_token = self.token
        self.store_token()
        return new_token





if __name__ == "__main__":
    token_manager = TokenManager()
    # token_manager.generate_token()
    # token_manager.store_token()
    token = token_manager.get_valid_token()
    print(token)

