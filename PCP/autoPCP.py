import csv
from collections import defaultdict

def read_promos(promo):
    if 'None' in promo:
        promo = ['3', '2', '1']
    student_list = list()
    for i in range(0, len(promo)):
        with open(f"./PCP/tek{promo[i]}_list.csv", mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            student_list.append([row[0] for row in reader])
    return student_list

def give_grade(Credits):
    if Credits >= 1:
        return 'Acquis'
    else:
        return 'Echec'

def give_credit(Total):
    if Total >= 3 and Total <= 6:
        return 1
    elif Total >= 7:
        return 2
    else:
        return 0

def pcp(args):
    student_list = read_promos([str(args.tek)])
    with open(args.filename, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        headers = next(reader)

        possibles_notes = ['2', '3', '4']
        data = defaultdict(lambda: {"presence": 0, "absence": 0, "not_registered": 0})
        for row in reader:
            login = row[0]
            if (login not in student_list[0]):
                continue
            for i in range(1, len(row)):
                if row[i] in possibles_notes:
                    data[login]["presence"] += 1
                elif row[i] == '-21' or row[i] == '1':
                    data[login]["absence"] += 1
                elif row[i] == '':
                    data[login]["not_registered"] += 1

    with open("PCP_output.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(['Login', 'Presence', 'Absence', 'Total', 'Credits', 'Grade'])
        for login in sorted(data):
            credits = give_credit(data[login]["presence"] - data[login]["absence"])
            grades = give_grade(credits)
            writer.writerow([login, data[login]["presence"], data[login]["absence"], data[login]["presence"] - data[login]["absence"], credits, grades])