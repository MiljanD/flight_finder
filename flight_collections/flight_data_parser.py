from flight_collections.flight_search_service import FlightSearchService



class FlightDataParser:
    """
    Parses raw flight data into structured format for storage and analysis.
    """
    def __init__(self):
        self.flight_data = FlightSearchService()


    def parse_flight_data(self) -> list:
        """
        Parses raw flight data into structured format for storage and analysis.
        :return: structured list of flights data
        """
        flight_data = self.flight_data.flight_details_collection()
        flight_details = []
        for data in flight_data:
            try:
                for content in data["data"]:
                    departure = None
                    arrival = None
                    transfers = []

                    for segment in content["itineraries"]:
                        segments = segment["segments"]
                        departure = segments[0]["departure"]
                        arrival = segments[0]["arrival"]

                        if len(segments) > 1:
                            for seg in segments[1:]:
                                transfers.append({"departure":seg["departure"], "arrival": seg["arrival"]})

                    price = content["price"]["grandTotal"]
                    data = {"departure": departure, "arrival": arrival, "price": price, "transfers": transfers}
                    flight_details.append(data)
            except KeyError:
                raise KeyError ("Neispravan kljuc u odzivu API servisa.")

        return flight_details
