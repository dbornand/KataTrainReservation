from unittest.mock import patch

import pytest

from ticket_office import TicketOffice


@pytest.fixture(autouse=True)
def mock_select_seats():
    with patch.object(TicketOffice, 'select_seats') as mock_select_seats:
        yield mock_select_seats


@pytest.fixture(autouse=True)
def mock_get_booking_reference():
    with patch.object(TicketOffice, 'get_booking_reference') as mock_get_booking_reference:
        yield mock_get_booking_reference


@pytest.fixture(autouse=True)
def mock_trigger_reservation():
    with patch.object(TicketOffice, 'trigger_reservation') as mock_trigger_reservation:
        yield mock_trigger_reservation


def test_assert_train_id_is_returned_in_reservation():
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('foo_train', 1)
    assert reservation["train_id"] == 'foo_train'


def test_booking_reference_is_empty_if_no_suitable_seats_are_found(mock_select_seats, mock_get_booking_reference):
    mock_get_booking_reference.return_value = 'a1b2c3'
    mock_select_seats.return_value = []
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('foo_train', 1)
    assert reservation["booking_reference"] == ''


def test_booking_reference_is_returned_if_suitable_seats_are_found(mock_select_seats, mock_get_booking_reference):
    mock_get_booking_reference.return_value = "a1b2c3"
    mock_select_seats.return_value = ["1A"]
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('foo_train', 1)
    assert reservation["booking_reference"] == "a1b2c3"


def test_selected_seats_are_returned_in_reservation(mock_select_seats):
    mock_select_seats.return_value = ["1A", "2A"]
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('foo_train', 2)
    assert reservation["seats"] == ["1A", "2A"]


def test_reservation_is_triggered_if_suitable_seats_are_found(mock_select_seats, mock_trigger_reservation):
    mock_select_seats.return_value = ["1A", "2A"]
    ticket_office = TicketOffice()
    ticket_office.reserve('foo_train', 2)
    mock_trigger_reservation.assert_called_once()


def test_reservation_is_not_triggered_if_no_suitable_seats_are_found(mock_select_seats, mock_trigger_reservation):
    mock_select_seats.return_value = []
    ticket_office = TicketOffice()
    ticket_office.reserve('foo_train', 1)
    mock_trigger_reservation.assert_not_called()

# SINGLE COACH, NO RESERVATION
# one seat
# __________ +1
# x_________
# multiple seats
# __________ +3
# xxx_______
# can reserve coach max capacity
# __________ +7
# xxxxxxx___
# cannot reserve above coach max capacity
# __________ +8
# __________
# SINGLE COACH, WITH RESERVATIONS
# one seat
# z_________ +1
# zx________
# multiple seats
# _z________ +3
# xzxx______
# can reserve up to coach max capacity
# zzzz_z____ +2
# zzzzxzx___
# cannot reserve above coach max capacity
# zzzzzz____ +2
# zzzzzz____
# MULTIPLE COACHES, NO RESERVATIONS
# can reserve in first coach
# _____ __________ +3
# xxx___ __________
# reserve in next coach if coach capacity is reached
# _____ __________ +7
# _____ xxxxxxx____
# can override coach max capacity
# __________ __________ +10
# xxxxxxxxxx __________
# cannot split a single reservation
# __________ __________ +11
# __________ __________
# MULTIPLE COACHES, WITH RESERVATIONS
# reserve in next coach if coach capacity is reached
# zzzzzz____ __________ +2
# zzzzzz____ xx________
# can override coach capacity
# zzzzzz____ zzzzzz____ +2
# zzzzzzxx__ zzzzzz____
# cannot reserve above train max capacity
# zzzzzzzz__ zzzzzz____ +1
# zzzzzzzz__ zzzzzz____
