import requests


class TicketOffice:

    def reserve(self, train_id, seat_count):
        selected_seats = self.select_seats(train_id, seat_count)
        if selected_seats:
            booking_reference = self.get_booking_reference()
        else:
            booking_reference = ""
        reservation = {
            "train_id": train_id,
            "booking_reference": booking_reference
        }
        return reservation

    def get_booking_reference(self):
        url = "http://127.0.0.1:8082" + "/booking_reference"
        response = requests.get(url)
        booking_reference = response.text
        return booking_reference

    def select_seats(self, train_id, seat_count):
        # TODO Implement
        raise NotImplementedError


if __name__ == "__main__":
    """Deploy this class as a web service using CherryPy"""
    import cherrypy

    TicketOffice.reserve.exposed = True
    cherrypy.config.update({"server.socket_port": 8083})
    cherrypy.quickstart(TicketOffice())
