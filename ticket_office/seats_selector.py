class Seat:

    def __init__(self, seat_id, booking_reference=""):
        self.booking_reference = booking_reference
        self.id = seat_id


class Coach:
    def __init__(self, coach_id, seats):
        self.id = coach_id
        self.seats = seats

    @property
    def available_seats(self):
        return [seat for seat in self.seats if not seat.booking_reference]

    @property
    def reserved_seats(self):
        return [seat for seat in self.seats if seat.booking_reference]


class Train:
    def __init__(self, train_id, coaches):
        self.id = train_id
        self.coaches = coaches

    @property
    def seats(self):
        return [seat for coach in self.coaches for seat in coach.seats]

    @property
    def available_seats(self):
        return [seat for coach in self.coaches for seat in coach.available_seats]

    @property
    def reserved_seats(self):
        return [seat for coach in self.coaches for seat in coach.reserved_seats]


def select_seats(train_id, seat_count):
    train = get_train(train_id)

    selected_seats = []
    for coach in train.coaches:
        selected_seats = _select_coach_seats(coach, seat_count, max_capacity=0.7)
        if selected_seats:
            break

    if not selected_seats:
        for coach in train.coaches:
            selected_seats = _select_coach_seats(coach, seat_count, max_capacity=1.0)
            if selected_seats:
                break

    if len(selected_seats) + len(train.reserved_seats) > 0.7 * len(train.seats):
        return []

    return [seat.id for seat in selected_seats]


def _select_coach_seats(coach, seat_count, max_capacity=1.0):
    if seat_count > len(coach.seats):
        return []
    selected_seats = coach.available_seats[:seat_count]
    if len(selected_seats) + len(coach.reserved_seats) > max_capacity * len(coach.seats):
        selected_seats = []
    return selected_seats


def get_train(train_id):
    # TODO Implement
    raise NotImplementedError
