from unittest.mock import patch

import pytest

from seats_selector import select_seats


class TrainBuilder:

    def __init__(self):
        self.reserved_seats = []
        self.coaches = []

    def build_seats(self):
        train_seats = dict()
        for coach_id, number_of_seats in self.coaches:
            for seat_number in range(1, number_of_seats + 1):
                seat_id = str(seat_number) + coach_id
                if seat_id in self.reserved_seats:
                    booking_reference = "already_reserved_seat"
                else:
                    booking_reference = ''
                seat_data = {"booking_reference": booking_reference, "seat_number": str(seat_number), "coach": coach_id}
                train_seats[seat_id] = seat_data
        return train_seats

    def with_coach(self, coach_id, number_of_seats):
        self.coaches.append((coach_id, number_of_seats))
        return self

    def reserve(self, seats_id):
        for seat_id in seats_id:
            self.reserved_seats.append(seat_id)
        return self


@pytest.fixture(autouse=True)
def mock_get_train_seats():
    with patch('seats_selector.get_train_seats') as mock_get_train_seats:
        yield mock_get_train_seats


def test_select_one_seat_in_an_empty_coach(mock_get_train_seats):
    builder = TrainBuilder()
    builder.with_coach('A', 10)
    train_seats = builder.build_seats()
    mock_get_train_seats.return_value = train_seats
    seats = select_seats('foo_train', 1)
    assert seats == ["1A"]


def test_select_up_to_max_capacity_in_an_empty_coach(mock_get_train_seats):
    builder = TrainBuilder()
    train_seats = builder.with_coach('A', 10).build_seats()
    mock_get_train_seats.return_value = train_seats
    seats = select_seats('foo_train', 7)
    assert len(seats) == 7
    assert "1A" in seats
    assert "7A" in seats
