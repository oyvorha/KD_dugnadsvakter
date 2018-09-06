
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd


def make_shifts_dict():
    eposter = ""
    dict_people = {}
    df_people = pd.read_excel('name.xlsx', sheet_name="Sheet1")
    for index, row in df_people.iterrows():
        if row['Navn'] not in dict_people.keys():
            eposter += str(row['epost']) + ";"
            dict_people[row['Navn']] = []
            dict_people[row['Navn']].append(row['epost'])
            dict_people[row['Navn']].append([row['Vakt'] + "\n \tFra: " + row['Fra']
                                            + ", Til: " + row['Til'] + "\n \tOppmøtested: " + row['Antrekk']
                                            + ", Antrekk: " + row['Oppmøtested'] + ", Beskrivelse: " + row['Beskrivelse']])
        else:
            dict_people[row['Navn']][1].append(row['Vakt'] + "\n \t Fra: " + row['Fra']
                                             + ", Til: " + row['Til'] + "\n \tOppmøtested: " + row['Antrekk']
                                             + ", Antrekk: " + row['Oppmøtested'] + ", Beskrivelse: " + row[
                                                 'Beskrivelse'])
    return dict_people, eposter


def make_body(person, vakter):
    text = "Hei " + person.split()[0] + "! \n \nHer er dine dugnadsvakter: \n \n"
    for i in range(len(vakter)):
        text += "Vakt " + str(i+1) + ": " + vakter[i] + "\n \n"
    text += "Mvh \nIndex-styret"
    return text


def send_to_all(dict_people):
    for person in dict_people.keys():
        fromaddr = "username@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['Subject'] = "Her er dine dugnadsvakter for KD"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "password")
        toaddr = dict_people[person][0]
        msg['To'] = dict_people[person][0]
        msg.attach(MIMEText(make_body(person, dict_people[person][1]), 'plain'))
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()


dict_ppl, eposter = make_shifts_dict()
send_to_all(dict_ppl)
