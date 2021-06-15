import requests


class Coach:

    def __init__(self, coach_id, seats):
        self.id = coach_id
        self.seats = seats


class Seat:

    def __init__(self, seat_id, booking_reference):
        self.id = seat_id
        self.booking_reference = booking_reference


def select_seats(train_id, seat_count):
    train_seats = get_train_seats(train_id)
    selected_seats = list(train_seats.keys())[:seat_count]
    return selected_seats


def get_train_seats(train_id):
    url = "http://127.0.0.1:8081/data_for_train/" + train_id
    response = requests.get(url)
    train_data = response.json()
    train_seats = train_data["seats"]
    return train_seats
