from datetime import datetime
import random

# Changes the time in the GEDCOM to a datetime format

def time_modification(time_str):
    if 'ABT' in time_str:
        if len(time_str) == 8:
            annee = int(time_str[4:])
            mois = random.randint(1,12)
            jour = random.randint(1,28)
        elif len(time_str) == 15:
            annee = int(time_str[11:])
            datetime_object = datetime.strptime(time_str[7:10], "%b")
            mois = datetime_object.month
            jour = int(time_str[4:6])
        elif len(time_str) == 12:
            annee = int(time_str[8:])
            mois = random.randint(1, 12)
            jour = random.randint(1, 28)
    elif 'BEF' in time_str:
        if len(time_str) == 8:
            annee = int(time_str[4:])-1
            mois = random.randint(1,12)
            jour = random.randint(1,28)
        elif len(time_str) == 15:
            annee = int(time_str[11:])
            datetime_object = datetime.strptime(time_str[7:10], "%b")
            mois = datetime_object.month
            jour = int(time_str[4:6])
    elif time_str == '31 NOV 1768':
        annee = 1768
        mois = 11
        jour = 30
    elif len(time_str) == 4:
        annee = int(time_str)
        mois = random.randint(1,12)
        jour = random.randint(1,28)
    elif len(time_str) == 8:
        annee = int(time_str[4:])
        datetime_object = datetime.strptime(time_str[0:3], "%b")
        mois = datetime_object.month
        jour = random.randint(1,28)
    else:
        annee = int(time_str[7:])
        datetime_object = datetime.strptime(time_str[3:6], "%b")
        mois = datetime_object.month
        jour = int(time_str[0:2])

    return datetime(annee,mois,jour)