from _datetime import timedelta


class Person:

    work_threshold = 34

    def __init__(self, person_id, epost, name, strength):
        self.id = person_id
        self.name = name
        self.email = epost
        self.strength = strength
        self.hours_work = 0
        self.shifts = []
        self.night_thres = 0

    def add_shift(self, shift):
        self.shifts.append(shift)
        self.hours_work += (shift.hours * shift.weight)
        shift.allocated = True
        if shift.responsibility.id == 1:
            self.night_thres += 1

    def check_add_shift(self, shift):
        if shift.allocated:
            return False
        if (self.hours_work + shift.hours * shift.weight) > Person.work_threshold:
            return False
        if shift.responsibility.strength == 1 and self.strength == 0:
            return False
        if shift.responsibility.id == 1 and self.night_thres > 1:
            return False

        for vakt in self.shifts:
            if shift.responsibility.strength == 1 and vakt.responsibility.strength == 1:
                # Du skal ikke ha en tung vakt dagen før eller dagen etter.
                if -2 < vakt.time_to.day - shift.time_from.day < 2:
                    return False
            # Check 30 min in between shifts
            if (vakt.time_from - timedelta(minutes=30) <
                shift.time_from < vakt.time_to + timedelta(
                    minutes=30)) or (vakt.time_from - timedelta(
            minutes=30) < shift.time_to < vakt.time_to + timedelta(minutes=30)):
                return False
            if vakt.time_from > shift.time_from and vakt.time_to < shift.time_to:
                return False
            if shift.responsibility.id == 1:
                # Make sure night shift is not added to busy day --> add heavy shifts first in alg
                if (vakt.time_from - timedelta(hours=6) <
                        shift.time_from < vakt.time_to + timedelta(
                        hours=6)) or (vakt.time_from - timedelta(
                        minutes=6) < shift.time_to < vakt.time_to + timedelta(minutes=6)):
                    return False
        return True

    def __str__(self):
        return "Navn: {}, Timer totalt: {}, Shifts: {}".format(self.name, self.hours_work, self.shifts)
