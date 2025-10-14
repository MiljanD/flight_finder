from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime, timedelta
import requests
from models.db import Db
from exports.exporter import Exporter

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class TokenManager(Db):
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


    def generate_token(self):
        parameters = {
            "grant_type": "client_credentials",
            "client_id": TokenManager.api_key,
            "client_secret": TokenManager.api_secret
        }

        headers = {
            "content-type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url=TokenManager.token_endpoint, data=parameters, headers=headers)
        if response.status_code == 200:
            token_data = response.json()

            self.token = token_data["access_token"]
            self.generated_at = datetime.now()
            self.expires = datetime.now() + timedelta(seconds=token_data["expires_in"] - 60)


    def reset_token_data(self):
        self.token = None
        self.generated_at = None
        self.expires = None


    def store_token(self):
        with self.con.cursor() as cursor:
            query = ("INSERT INTO tokens (token, created_at, expire, status) "
                     "VALUES (%s, %s, %s, %s)")
            cursor.execute(query, (self.token, self.generated_at, self.expires, "active"))
            self.con.commit()

        self.reset_token_data()


    def update_token_status(self):
        all_tokens = self.exports.get_all_tokens()
        for current_token in all_tokens:
            if current_token["expire"] < datetime.now() and current_token["status"] == "inactive":
                with self.con.cursor() as cursor:
                    query = "UPDATE tokens SET status=%s WHERE id=%s"
                    cursor.execute(query, ("inactive", current_token["id"]))
                    self.con.commit()



    def get_valid_token(self):
        # prvo azuriramo statuse
        # ako nema aktivan token generisemo novi i vratimo ga
        # ako ima aktivan vratimo aktivan
        pass






if __name__ == "__main__":

    token_manager = TokenManager()
    token_manager.update_token_status()

