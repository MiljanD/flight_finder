from datetime import datetime


class DateConverter:


    def convert_str_dash_separated(self, str_date):
        date_format = "%Y-%m-%d"
        converted_date = datetime.strptime(str_date, date_format).date()
        return converted_date


    def is_passed_date(self, str_date):
        return self.convert_str_dash_separated(str_date) < datetime.now().date()

