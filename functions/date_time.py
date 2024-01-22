from datetime import datetime


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


if __name__ == '__main__':
    date_str = "2022年12月02日 - 02:04:32"
    formatted_datetime = format_string_to_datetime(date_str)
    timestamp = formatted_datetime.timestamp()
    print(timestamp)
