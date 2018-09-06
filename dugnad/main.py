import read_file
from random import shuffle
import math
import pandas as pd
import copy
import timeout_decorator

people_org, heavy_shifts_org, night_shifts_org, other_shifts_org = read_file.get_info()
avg_hours = 33


@timeout_decorator.timeout(2)
def allocate():
    people = copy.deepcopy(people_org)
    heavy_shifts = copy.deepcopy(heavy_shifts_org)
    while heavy_shifts:
        shift_heavy = heavy_shifts[0]
        for person in people:
            if person.check_add_shift(shift_heavy):
                person.add_shift(shift_heavy)
                heavy_shifts.remove(shift_heavy)
        shuffle(people)
    night_shifts = copy.deepcopy(night_shifts_org)
    while night_shifts:
        shift_night = night_shifts[0]
        for person in people:
            if person.check_add_shift(shift_night):
                person.add_shift(shift_night)
                night_shifts.remove(shift_night)
        shuffle(people)
    other_shifts = copy.deepcopy(other_shifts_org)
    while other_shifts:
        shift_other = other_shifts[0]
        for person in people:
            if person.check_add_shift(shift_other):
                person.add_shift(shift_other)
                other_shifts.remove(shift_other)
        shuffle(other_shifts)
    print("Iteration Done")
    return people


def mean_square_error(people_list):
    error = 0
    for person in people_list:
        error += (person.hours_work-avg_hours)**2
    return error/2


def iterate():
    try:
        people = allocate()
    except Exception as e:
        return people_org, math.inf
    msq = mean_square_error(people)
    return people, msq


def write_to_file(people_list):
    rows = []
    for person in people_list:
        for shift in person.shifts:
            entry = [person.name, person.email, shift.responsibility.name, shift.responsibility.id, shift.time_from.strftime('%b %d %Y %H:%M'),
                     shift.time_to.strftime('%b %d %Y %H:%M'), shift.hours, shift.place, shift.outfit,
                     shift.responsibility.description, person.hours_work]
            rows.append(entry)
    df = pd.DataFrame(rows,
                      columns=['Navn', 'epost', 'Vakt', 'Vakt_id', 'Fra', 'Til', 'Lengde', 'Oppmøtested', 'Antrekk', 'Beskrivelse',
                               'totalt_person'])
    writer = pd.ExcelWriter('vaktliste.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()


def main():
    lowest_msq = math.inf
    best_shifts = people_org
    for i in range(100):
        people, msq = iterate()
        if msq < lowest_msq:
            lowest_msq = msq
            best_shifts = people
    print(lowest_msq)
    total_hours = 0
    for person in best_shifts:
        for shift in person.shifts:
            total_hours += shift.hours
    print(total_hours)
    write_to_file(best_shifts)


if __name__ == '__main__':
    main()
