from datetime import datetime

import discord
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


async def get_or_create_message(channel, title, description):
    async for message in channel.history(limit=1):
        # If there's an existing message, use that message
        return message

    # If no existing message, send a new one
    embed = discord.Embed(title=title, description=description)
    return await channel.send(embed=embed)


def seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds


def percentage_bar(percentage, bar_length=20, fill_char="■", empty_char="-"):
    progress = int(bar_length * percentage)
    bar = "[" + fill_char * progress + empty_char * (bar_length - progress) + "]"
    return f"{bar} {percentage * 100:.2f}%"


if __name__ == "__main__":
    bar = percentage_bar(0.7, 20, '■', '－')
    print(bar)
    # def cal(char):
    #     rs = '['
    #     for i in range(20):
    #         rs += char
    #     rs += "]"
    #     print(rs)
    #
    # cal('-')
    # cal('=')
    # cal('_')
    # cal('+')
    # cal('■')
    # cal('□')
    pass
