import json

from flask import Flask, request

from ticket_office import TicketOffice

app = Flask(__name__)

TICKET_OFFICE = None


@app.route('/reserve', methods=['POST'])
def reserve():
    train_id = request.form["train_id"]
    seat_count = int(request.form["seat_count"])
    reservation = TICKET_OFFICE.reserve(train_id, seat_count)
    return json.dumps(reservation)


def start():
    global TICKET_OFFICE
    TICKET_OFFICE = TicketOffice()

    app.config["SERVER_NAME"] = "127.0.0.1:8083"
    app.config["DEBUG"] = True
    app.run()


if __name__ == '__main__':
    start()
