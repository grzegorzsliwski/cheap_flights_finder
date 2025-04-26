from user_data import user_data_json
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()


TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")
TEQUILA_ENDPOINT = os.getenv("TEQUILA_ENDPOINT")



def get_iata_code(city_name):
    location_query_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
    headers = {"apikey": TEQUILA_API_KEY}
    params = {"term": city_name, "location_types": "city"}

    try:
        response = requests.get(url=location_query_endpoint, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()
        if "locations" in data and data["locations"]:
            iata_code = data["locations"][0]["code"]
            return iata_code
        else:
            raise ValueError(f"No IATA code found for city: {city_name}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as val_err:
        print(val_err)
    except Exception as err:
        print(f"An error occurred: {err}")

    return None


def get_flight_data(min_days, max_days, from_where, final_destination, max_stopovers, max_price):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    formatted_tomorrow = (f"{tomorrow.strftime('%d')}/"
                          f"{tomorrow.strftime('%m')}/"
                          f"{tomorrow.strftime('%Y')}")
    six_months_from_tomorrow = tomorrow + datetime.timedelta(days=6 * 30)
    formatted_six_months_from_tomorrow = (f"{six_months_from_tomorrow.strftime('%d')}/"
                                          f"{six_months_from_tomorrow.strftime('%m')}/"
                                          f"{six_months_from_tomorrow.strftime('%Y')}")

    fly_from = get_iata_code(from_where)
    fly_to = get_iata_code(final_destination)

    search_endpoint = f"{TEQUILA_ENDPOINT}/search"
    headers = {"apikey": TEQUILA_API_KEY}
    params = {"fly_from": fly_from,
              "fly_to": fly_to,
              "date_from": formatted_tomorrow,
              "date_to": formatted_six_months_from_tomorrow,
              "nights_in_dst_from": min_days,
              "nights_in_dst_to": max_days,
              "limit": 1,
              "curr": "PLN",
              "max_stopovers": max_stopovers,
              "price_to": max_price
              }
    response = requests.get(url=search_endpoint, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()["data"]
    print(data)
    return data
