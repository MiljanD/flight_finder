from models.flight_data_storage import FlightDataStorage
from models.travels import Travels
from notifier.EmailNotifier import EmailNotifier
from prompts.display_prompts import DisplayPrompts


class TravelCLI:
    """
    Orchestrates the command-line interface for managing travel-related operations.
    This class connects user prompts, travel data entry, flight information retrieval,
    terminal display, and email notification into a unified interactive loop.
    """
    def __init__(self):
        """
        Initializes the CLI controller with all required components.

        - Travels: handles user travel input and storage
        - EmailNotifier: sends formatted flight data via email
        - DisplayPrompts: manages user interaction and terminal display
        - FlightDataStorage: retrieves flight information from external sources

        """
        self.travels = Travels()
        self.notifier = EmailNotifier()
        self.viewer = DisplayPrompts()
        self.flights = FlightDataStorage()


    def run(self) -> None:
        """
        Starts the main CLI loop, prompting the user for actions and executing corresponding logic.

        Available options:
        1. Add travel details
        2. Fetch flight information
        3. Display flight table in terminal
        4. Send email notification
        5. Exit application
        """

        is_running = True
        while is_running:
            user_choice = self.viewer.show_home()

            # Option 1: Add travel details
            if user_choice == "1":
                travel_data = self.viewer.add_travel_data()
                self.travels.location_from = travel_data["location"]
                self.travels.location_from_code = travel_data["location_code"]
                self.travels.destination = travel_data["destination"]
                self.travels.destination_code = travel_data["destination_code"]
                self.travels.travel_date = travel_data["travel_date"]
                self.travels.passenger_number = travel_data["passengers"]
                self.travels.desired_price = travel_data["desired_price"]

                self.travels.store_travel_details()

            # Option 2: Fetch flight information
            elif user_choice == "2":
                self.travels.delete_passed_travel_details()
                self.flights.flight_data_storage()

            # Option 3: Display flight table in terminal
            elif user_choice == "3":
                self.viewer.display_table()

            # Option 4: Send email notification
            elif user_choice == "4":
                notification = self.viewer.send_notification()
                if notification:
                    self.notifier.send_email()

            # Option 5: Exit application
            elif user_choice == "5":
                print("Exiting...")
                is_running = False









