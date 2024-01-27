import requests

from config import *

stage = 1
mode_str = "kz_timer"

api_url = f"{GLOBAL_API_URL}api/v2.0/records/top?&{STEAMID}steamid64={None}&tickrate=128&stage={stage}&modes_list_string={mode_str}"

response = requests.get(api_url)

if response.status_code == 200:
    # Request was successful
    print("Response:", len(response.text))
else:
    # Request encountered an error
    print("Error:", response.status_code, response.text)
