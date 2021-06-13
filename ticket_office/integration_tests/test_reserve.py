import pytest
import requests

from ticket_office import TicketOffice


@pytest.fixture(autouse=True)
def reset_trains():
    train_id = 'express_2000'
    url = "http://127.0.0.1:8081/reset/" + train_id
    requests.get(url)


def test_reserve_one_seat_in_express_2000():
    ticket_office = TicketOffice()
    reservation = ticket_office.reserve('express_2000', 1)
    assert reservation["train_id"] == 'express_2000'
    assert reservation["booking_reference"] != ""
    assert reservation["seats"] == ["1A"]


def test_reserve_service():
    url = "http://127.0.0.1:8083/reserve"
    data = {"train_id": "express_2000", "seat_count": "1"}
    response = requests.post(url, data=data)
    assert response.status_code == 200
