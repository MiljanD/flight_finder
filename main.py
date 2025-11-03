from cli.travel_cli import TravelCLI


if __name__ == "__main__":
    """
    Entry point for the TravelCLI application.

    Initializes the CLI controller and starts the interactive loop for managing travel data,
    fetching flight information, displaying tables, and sending notifications.
    """
    app = TravelCLI() # Create CLI controller instance

    app.run() # Start the main application loop



