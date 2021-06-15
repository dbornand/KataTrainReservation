from unittest.mock import patch

import pytest

from ticket_office import TicketOffice


@pytest.fixture(autouse=True)
def mock_select_seats():
    with patch('ticket_office.select_seats') as mock_select_seats:
        yield mock_select_seats


@pytest.fixture(autouse=True)
def mock_get_booking_reference():
    with patch.object(TicketOffice, 'get_booking_reference') as mock_get_booking_reference:
        yield mock_get_booking_reference


@pytest.fixture(autouse=True)
def mock_trigger_reservation():
    with patch.object(TicketOffice, 'trigger_reservation') as mock_trigger_reservation:
        yield mock_trigger_reservation


def test_train_id_is_returned_in_reservation():
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('foo_train', 1)
    assert reservation["train_id"] == 'foo_train'


def test_booking_reference_is_empty_if_no_suitable_seats_are_found(mock_select_seats):
    mock_select_seats.return_value = []
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('foo_train', 1)
    assert reservation["booking_reference"] == ''


def test_non_empty_booking_reference_is_returned_if_suitable_seats_are_found(mock_select_seats,
                                                                             mock_get_booking_reference):
    mock_get_booking_reference.return_value = 'a1b2c3'
    mock_select_seats.return_value = ["1A"]
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('foo_train', 1)
    assert reservation["booking_reference"] == 'a1b2c3'


def test_selected_seats_are_returned(mock_select_seats):
    mock_select_seats.return_value = ["1A", "2A"]
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('foo_train', 2)
    assert reservation["seats"] == ["1A", "2A"]


def test_reservation_is_triggered_if_suitable_seats_are_found(mock_select_seats, mock_trigger_reservation):
    mock_select_seats.return_value = ["1A"]
    ticket_office = TicketOffice()
    ticket_office.reserve('foo_train', 1)
    mock_trigger_reservation.assert_called_once()


def test_reservation_is_not_triggered_if_no_suitable_seats_are_found(mock_select_seats, mock_trigger_reservation):
    mock_select_seats.return_value = []
    ticket_office = TicketOffice()
    ticket_office.reserve('foo_train', 1)
    mock_trigger_reservation.assert_not_called()
