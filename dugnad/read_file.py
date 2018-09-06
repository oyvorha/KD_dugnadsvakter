from Person import Person
from Shift import Shift
from Ansvar import Ansvar
import pandas as pd
import datetime


people = []
shifts = []
heavy_shifts = []
night_shifts = []
other_shifts = []
ansvar = {}


def read_file():
    format = "%d.%m.%Y %H:%M:%S"
    df_people = pd.read_excel('Index-progg.xlsx', sheet_name="Personer")
    for index, row in df_people.iterrows():
        pers = Person(row['id'], row['brukernavn'], row['navn'], row['strength'])
        people.append(pers)
    df_ansvar = pd.read_excel('Index-progg.xlsx', sheet_name="Ansvar")
    for index, row in df_ansvar.iterrows():
        ansvar[row['id']] = Ansvar(row['id'], row['navn'], row['strength'], row['beskrivelse'])
    df_shifts = pd.read_excel('Index-progg.xlsx', sheet_name="Vakt")
    for index, row in df_shifts.iterrows():
        date_from = datetime.datetime.strptime(str(row['dato_fra'].day) + '.' + str(row['dato_fra'].month) + '.' + str(row['dato_fra'].year)
                                  + ' ' + str(row['tid_fra']), format)
        date_to = datetime.datetime.strptime(str(row['dato_til'].day) + '.' + str(row['dato_til'].month) + '.' + str(row['dato_til'].year)
                                + ' ' + str(row['tid_til']), format)
        shifts.append(Shift(row['id'], ansvar[int(row['ansvar'])], date_from, date_to,
                           row['antall_timer'], row['weight'], row['antrekk'],
                                   row['oppmøtested']))


def pre_allocate():
    # index equals shift id for shifts[index]
    df_pre_allocate = pd.read_excel('Index-progg.xlsx', sheet_name="VaktPerson")
    for index, row in df_pre_allocate.iterrows():
        people[int(row['person_id']-1)].add_shift(shifts[int(row['vakt_id']-1)])
        # print(people[int(row['person_id']-1)])
        # for shift in people[int(row['person_id']-1)].shifts:
        #     print(shift.responsibility.name)


def sort_shifts():
    for shift in shifts:
        if shift.allocated:
            continue
        if shift.responsibility.strength == 1:
            heavy_shifts.append(shift)
            continue
        if shift.responsibility.id == 1:
            night_shifts.append(shift)
            continue
        other_shifts.append(shift)


def get_info():
    read_file()
    pre_allocate()
    sort_shifts()
    return people, heavy_shifts, night_shifts, other_shifts


def write_shifts(shifts):
    rows = []
    for shift in shifts:
        entry = [shift.responsibility.name, shift.time_from.strftime('%b %d %Y %H:%M'),
                 shift.time_to.strftime('%b %d %Y %H:%M'), shift.hours, shift.place, shift.outfit,
                 shift.responsibility.description]
        rows.append(entry)
    df = pd.DataFrame(rows,
                      columns=['Vakt', 'Fra', 'Til', 'Lengde', 'Oppmøtested', 'Antrekk', 'Beskrivelse'])
    writer = pd.ExcelWriter('vakter.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Vakter')
    writer.save()
