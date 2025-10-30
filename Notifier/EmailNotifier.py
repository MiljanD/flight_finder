import smtplib
from email.message import EmailMessage
from dotenv import find_dotenv, load_dotenv
import os
from exports.exporter import Exporter
from prettytable import PrettyTable


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class EmailNotifier:
    def __init__(self):
        self.exports = Exporter()


    def generate_flights_table(self):
        flights_table = PrettyTable()
        flights_data = self.exports.export_complete_flights_data()

        columns = [key for key, value in flights_data[0].items()]
        flights_table.field_names = columns

        for data in flights_data:
            row_data = []
            for column in columns:
                row_data.append(data[column])

            flights_table.add_row(row_data)


        return flights_table.get_html_string(attributes={"style": "text-align:center;"})


    def send_email(self):
        sender = os.getenv("SENDER_EMAIL")
        receiver = os.getenv("RECEIVER_EMAIL")
        app_password = os.getenv("APP_PASSWORD")

        table_content = self.generate_flights_table()
        email = EmailMessage()
        email["Subject"] = "Flights"
        email["From"] = sender
        email["To"] = receiver
        host_provider = os.getenv("EMAIL_PROVIDER_HOST")
        port = os.getenv("PORT")
        email.set_content(table_content, subtype="html")

        with smtplib.SMTP(host_provider, port) as connection:
            connection.starttls()
            connection.login(user=sender, password=app_password)
            connection.send_message(email)






if __name__ == "__main__":
    notifier = EmailNotifier()
    notifier.send_email()