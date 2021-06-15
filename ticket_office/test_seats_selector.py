from unittest.mock import patch

import pytest

from seats_selector import select_seats, Seat, Coach, Train


@pytest.fixture(autouse=True)
def mock_get_train():
    with patch('seats_selector.get_train') as mock_get_train:
        yield mock_get_train


class TrainBuilder:

    def __init__(self, train_id):
        self.train_id = train_id
        self.coaches = []
        self.reserved_seats = []

    def with_coach(self, coach_id, seat_count):
        self.coaches.append((coach_id, seat_count))
        return self

    def reserve(self, *seats_id):
        for seat_id in seats_id:
            self.reserved_seats.append(seat_id)
        return self

    def build(self):
        coaches = []
        for coach_id, seat_count in self.coaches:
            coach = self._build_coach(coach_id, seat_count)
            coaches.append(coach)
        train = Train(self.train_id, coaches)
        return train

    def _build_coach(self, coach_id, seat_count):
        coach_seats = []
        for seat_number in range(1, seat_count + 1):
            seat = self._build_seat(coach_id, seat_number)
            coach_seats.append(seat)
        coach = Coach(coach_id, coach_seats)
        return coach

    def _build_seat(self, coach_id, seat_number):
        seat_id = str(seat_number) + coach_id
        seat = Seat(seat_id)
        if seat_id in self.reserved_seats:
            seat.booking_reference = "foo_booking_ref"
        return seat


def test_select_one_seat_in_an_empty_coach(mock_get_train):
    builder = TrainBuilder('foo_train')
    mock_get_train.return_value = builder.with_coach("A", 10).build()
    seats = select_seats('foo_train', 1)
    assert seats == ["1A"]


def test_select_multiple_seats_in_an_empty_coach(mock_get_train):
    builder = TrainBuilder('foo_train')
    mock_get_train.return_value = builder.with_coach("A", 10).build()
    seats = select_seats('foo_train', 3)
    assert len(seats) == 3
    assert set(seats) == {"1A", "2A", "3A"}


def test_can_select_up_to_max_capacity_of_an_empty_coach(mock_get_train):
    builder = TrainBuilder('foo_train')
    mock_get_train.return_value = builder.with_coach("A", 10).build()
    seats = select_seats('foo_train', 7)
    assert len(seats) == 7
    assert set(seats) == {"1A", "2A", "3A", "4A", "5A", "6A", "7A"}


def test_cannot_select_above_max_capacity_of_an_empty_coach(mock_get_train):
    builder = TrainBuilder('foo_train')
    mock_get_train.return_value = builder.with_coach("A", 10).build()
    seats = select_seats('foo_train', 8)
    assert seats == []


def test_select_one_seat_in_a_coach_with_reservations(mock_get_train):
    builder = TrainBuilder('foo_train')
    train_seats = builder.with_coach("A", 10).reserve("1A").build()
    mock_get_train.return_value = train_seats
    seats = select_seats('foo_train', 1)
    assert seats == ["2A"]


def test_select_multiple_seats_in_a_coach_with_reservations(mock_get_train):
    builder = TrainBuilder('foo_train')
    train_seats = builder.with_coach("A", 10).reserve("2A").build()
    mock_get_train.return_value = train_seats
    seats = select_seats('foo_train', 3)
    assert len(seats) == 3
    assert set(seats) == {"1A", "3A", "4A"}


def test_select_up_to_max_capacity_in_a_coach_with_reservations(mock_get_train):
    builder = TrainBuilder('foo_train')
    train_seats = builder.with_coach("A", 10).reserve("1A", "2A", "3A", "4A", "6A").build()
    mock_get_train.return_value = train_seats
    seats = select_seats('foo_train', 2)
    assert len(seats) == 2
    assert set(seats) == {"5A", "7A"}


def test_cannot_select_above_max_capacity_in_a_coach_with_reservations(mock_get_train):
    builder = TrainBuilder('foo_train')
    train_seats = builder.with_coach("A", 10).reserve("1A", "2A", "3A", "4A", "5A", "6A").build()
    mock_get_train.return_value = train_seats
    seats = select_seats('foo_train', 2)
    assert seats == []


def test_select_multiple_seats_in_multiple_coaches(mock_get_train):
    builder = TrainBuilder('foo_train')
    train_seats = builder.with_coach("A", 10).with_coach("B", 10).build()
    mock_get_train.return_value = train_seats
    seats = select_seats('foo_train', 3)
    assert len(seats) == 3
    assert set(seats) == {"1A", "2A", "3A"}


def test_select_in_next_coach(mock_get_train):
    builder = TrainBuilder('foo_train')
    train_seats = builder.with_coach("A", 5).with_coach("B", 10).build()
    mock_get_train.return_value = train_seats
    seats = select_seats('foo_train', 7)
    assert len(seats) == 7
    assert set(seats) == {"1B", "2B", "3B", "4B", "5B", "6B", "7B"}


def test_can_override_coach_max_capacity(mock_get_train):
    builder = TrainBuilder('foo_train')
    train = builder.with_coach("A", 10).with_coach("B", 10).build()
    mock_get_train.return_value = train
    seats = select_seats('foo_train', 10)
    assert len(seats) == 10
    assert "1A" in seats
    assert "10A" in seats


def test_cannot_split_a_single_reservation(mock_get_train):
    builder = TrainBuilder('foo_train')
    train = builder.with_coach("A", 10).with_coach("B", 10).build()
    mock_get_train.return_value = train
    seats = select_seats('foo_train', 11)
    assert seats == []


def test_select_multiple_seats_in_coaches_with_reservations(mock_get_train):
    builder = TrainBuilder('foo_train')
    train = builder.with_coach("A", 10).with_coach("B", 10).reserve("1A", "2A", "3A", "4A", "5A", "6A").build()
    mock_get_train.return_value = train
    seats = select_seats('foo_train', 2)
    assert len(seats) == 2
    assert set(seats) == {"1B", "2B"}


def test_can_override_max_capacity_in_coaches_with_reservations(mock_get_train):
    builder = TrainBuilder('foo_train')
    builder.with_coach("A", 10).with_coach("B", 10)
    train = builder.reserve("1A", "2A", "3A", "4A", "5A", "6A").reserve("1B", "2B", "3B", "4B", "5B", "6B").build()
    mock_get_train.return_value = train
    seats = select_seats('foo_train', 2)
    assert len(seats) == 2
    assert set(seats) == {"7A", "8A"}


def test_cannot_select_above_train_max_capacity(mock_get_train):
    builder = TrainBuilder('foo_train')
    builder.with_coach("A", 10).with_coach("B", 10)
    builder.reserve("1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A").reserve("1B", "2B", "3B", "4B", "5B", "6B")
    mock_get_train.return_value = builder.build()
    seats = select_seats('foo_train', 1)
    assert seats == []
