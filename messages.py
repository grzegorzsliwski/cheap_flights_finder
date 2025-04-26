from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
ACC_SID = os.getenv("TWILIO_ACC_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")


class Messages:
    def __init__(self):
        self.client = Client(ACC_SID, AUTH_TOKEN)

    def send_message(self, fly_from, fly_to, city_from, city_to, formatted_departure_start_time, number_of_flights,
                     formatted_return_end_time, flight_price, number_of_stopovers_on_departure,
                     city_stopovers_on_departure, number_of_stopovers_on_arrival, city_stopovers_on_arrival):

        if number_of_flights <= 2:
            message = self.client.messages.create(
                from_=TWILIO_PHONE_NUMBER,
                to=MY_PHONE_NUMBER,
                body=f"Low price alert! Only {flight_price}zł to fly from {fly_from}-{city_from} to {fly_to}-{city_to}. "
                     f"Departure on {formatted_departure_start_time}, back in your place {formatted_return_end_time}."
            )
        else:
            message = self.client.messages.create(
                from_=TWILIO_PHONE_NUMBER,
                to=MY_PHONE_NUMBER,
                body=f"Low price alert! Only {flight_price}zł to fly from {fly_from}-{city_from} to {fly_to}-{city_to}. "
                     f"Departure on {formatted_departure_start_time}, back in your place {formatted_return_end_time}. "
                     f"Flight has {number_of_stopovers_on_departure} stopovers on departure, via "
                     f"{', '.join(city_stopovers_on_departure)} and {number_of_stopovers_on_arrival} "
                     f"stopovers on arrival, via {', '.join(city_stopovers_on_arrival)}"
            )
