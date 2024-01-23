from datetime import datetime
import pycountry


def get_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2 if country else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def format_string_to_datetime(date_string):
    """
    Converts a string in the format "YYYY年MM月DD日 - HH:MM:SS" to a datetime object.

    :param date_string: A string representing the date and time in the specified format.
    :return: A datetime object.
    """
    # Define the format string based on the input format
    format_str = '%Y年%m月%d日 - %H:%M:%S'
    # Use datetime.strptime to convert the string to a datetime object
    datetime_obj = datetime.strptime(date_string, format_str)
    return datetime_obj


def calculate_time_difference(join_date):
    # Get the current date and time
    current_date = datetime.now()

    # Calculate the difference between the current date and the join date
    delta = current_date - join_date

    # Calculate years, months, and days
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = delta.days % 30

    return years, months, days


if __name__ == "__main__":
    join_date_str = '2022-12-02 02:04:32'
    years, months, days = calculate_time_difference(join_date_str)
    print(f"Years: {years}, Months: {months}, Days: {days}")
