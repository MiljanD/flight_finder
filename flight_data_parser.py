from flight_search_service import FlightSearchService



class FlightDataParser:
    def __init__(self):
        self.flight_data = FlightSearchService()


    def parse_flight_data(self):
        flight_data = self.flight_data.flight_details_collection()
        for data in flight_data:
            for content in data["data"]:
                print(content["itineraries"])
                print(content["price"]["grandTotal"])






if __name__ == "__main__":
    parser = FlightDataParser()
    parser.parse_flight_data()