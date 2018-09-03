
class Shift:

    def __init__(self, id, ansvar, tid_fra, tid_til, antall_timer, weight, sted, antrekk):
        self.id = id
        self.responsibility = ansvar
        self.time_from = tid_fra
        self.time_to = tid_til
        self.hours = antall_timer
        self.weight = weight
        self.allocated = False
        self.place = sted
        self.outfit = antrekk

    def __str__(self):
        return "id: {}, responsibility id: {}, dato: {}, starttid: {}, sluttid: {}".format(
                self.id, self.responsibility, self.date_from, self.time_from, self.time_to)
