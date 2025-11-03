from notifier.EmailNotifier import EmailNotifier


class TerminalViewer:
    """
    Provides a terminal-based visualization of flight data.

    This class uses the EmailNotifier's table generation logic to retrieve structured flight data
    and display it in a readable format directly in the terminal using PrettyTable.
    """
    def __init__(self):
        """
        Initializes the TerminalViewer with access to the flight data exporter.
        Internally uses EmailNotifier to reuse the table generation logic.
        """
        self.display = EmailNotifier()

    def terminal_view(self) -> None:
        """
        Renders the flight data table in the terminal.
        Retrieves the PrettyTable object from EmailNotifier and prints it as a formatted string.
        """

        table = self.display.generate_flights_table()
        print(str(table))
