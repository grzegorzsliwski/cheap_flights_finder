from user_data import user_data_json
from flight import get_iata_code, get_flight_data
from messages import Messages
import datetime
from display_user_data import failed_to_send_messages, display_messages_sent


def format_datetime(timestamp):
    date_time = datetime.datetime.fromtimestamp(timestamp)
    return date_time.strftime('%d-%m-%Y')


def get_stopover_cities(flight_data, start_index, end_index):
    return [flight_data[0]["route"][i]["cityFrom"] for i in range(start_index, end_index)]


def search():
    user_data = user_data_json()
    messages_sent = False

    for user in user_data:
        destination_city_name = user["final_destination"]
        base_city_name = user["from_where"]

        from_where = get_iata_code(base_city_name)
        to_where = get_iata_code(destination_city_name)

        if not to_where or not from_where:
            continue

        flight_data = get_flight_data(user["min_days"], user["max_days"], from_where, to_where, user["max_stopovers"],
                                      user["max_price"])

        if not flight_data:
            continue

        flight = flight_data[0]
        departure_start_time = format_datetime(flight["dTimeUTC"])
        return_end_time = format_datetime(flight["route"][-1]["aTimeUTC"])

        index_to_city_to = next(
            index for index, route in enumerate(flight["route"]) if route["cityFrom"] == flight["cityTo"])

        city_stopovers_on_departure = get_stopover_cities(flight_data, 1, index_to_city_to)
        city_stopovers_on_arrival = get_stopover_cities(flight_data, index_to_city_to, len(flight["route"]))

        messages = Messages()
        messages.send_message(
            flight["flyFrom"], flight["flyTo"], flight["cityFrom"], flight["cityTo"], departure_start_time,
            len(flight["route"]), return_end_time, flight["price"],
            len(city_stopovers_on_departure), city_stopovers_on_departure,
            len(city_stopovers_on_arrival), city_stopovers_on_arrival
        )

        messages_sent = True

    if messages_sent:
        display_messages_sent()
    else:
        failed_to_send_messages()



# search()
