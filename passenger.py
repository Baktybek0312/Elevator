class Passenger(object):
    """
    пассажиры имеют основные атрибуты того, сколько времени это заняло,
    где они находятся, куда они хотят пойти, и удостоверение личности
    """
    def __init__(self, time_appeared=0., destination=1, pickup_floor=0, identity=0):
        self.pickup_floor = pickup_floor
        self.time_appeared = time_appeared
        self.time_exited = 0.
        self.destination = destination
        self.pickup_time = 0.
        self.identity = identity
        self.direction = "Up" if (self.destination - self.pickup_floor) > 0 else "Down"

    def set_time_exited(self, time_exited):
        self.time_exited = time_exited

    def set_pickup_time(self, pickup_time):
        self.pickup_time = pickup_time

    def get_pickup_time(self):
        return self.pickup_time

    def get_time_exited(self):
        return self.time_exited

    def get_time_appeared(self):
        return self.time_appeared

    def get_destination(self):
        return self.destination


class Building(object):
    """
    В каждом здании есть распределение людей, которые будут отобраны для создания пассажиров, а также
    общее количество пассажиров и количество этажей
    """
    def __init__(self, distribution_of_people, total_num_passengers):
        self.distribution_of_people = distribution_of_people
        self.floors = len(distribution_of_people)
        self.total_num_passengers = total_num_passengers

    def get_floors(self):
        return self.floors

    def get_distribution(self):
        return self.distribution_of_people

    def get_total_num_passengers(self):
        return self.total_num_passengers
