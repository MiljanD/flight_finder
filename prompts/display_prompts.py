from display.terminal_viewer import TerminalViewer


class DisplayPrompts:
    """
    Provides a command-line interface for user interaction.

    This class handles user prompts for adding travel details, viewing flight data in the terminal,
    and confirming email notifications. It serves as the interactive layer between the user and
    the underlying system logic.

    """

    home_options = ["Dodaj putovanje", "Prikupi informacije o letovima", "Prikaz letova", "Posalji notifikaciju", "Izlaz"]
    adding_params = {"location": "Polazna lokacija", "location_code": "IATA kod aerodroma polazne lokacije",
                     "destination": "Odrediste", "destination_code": "IATA kod aerodroma oderedista",
                     "travel_date": "Datum putovanja", "passengers": "Broj putnika", "desired_price": "Zeljena cena"}
    notification_options = ["Da", "Ne"]

    def __init__(self):
        """
        Initializes the DisplayPrompts interface.
        Sets up the terminal viewer for displaying flight data.
        """
        self.display = TerminalViewer()



    def show_home(self) -> str:
        """
        Displays the main menu options and prompts the user to select an action.
        :return: String representing the user's choice.
        """
        for idx, option in enumerate(self.home_options):
            print(f"{idx + 1}. {option}\n")
        user_choice = input(f"Izberite zeljenu opciju(1-{len(self.home_options)}): ")

        return user_choice


    def add_travel_data(self) -> dict:
        """
        Prompts the user to enter travel details required for flight search.
        :return: Dictionary containing user-provided travel parameters.
        """
        travel_data = {}
        date_format = "YYYY-MM-DD"
        for key, value in self.adding_params.items():
            if key == "travel_date":
                print(f"Datum mora biti u formi - {date_format}")
            user_input = input(f"{value}: ")
            travel_data[key] = user_input

        return travel_data


    def send_notification(self) ->bool:
        """
        Asks the user to confirm whether to send an email notification.
        :return: Boolean indicating user's confirmation.
        """
        for idx, option in enumerate(self.notification_options):
            print(f"{idx + 1}. {option}")

        user_choice = input(f"Da li sigurno zelite poslati notifikaciju(1-{len(self.notification_options)}): ")
        if user_choice == "1":
            return True
        return False


    def display_table(self):
        """
        Displays the current flight data table in the terminal using PrettyTable.
        """
        self.display.terminal_view()

