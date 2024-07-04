import csv
import argparse

def time_string_to_hours(time_string):
    hours, _, _ = map(int, time_string.split(':'))
    return hours


class Student:
    def __init__(self, login, logtime):
        self.login = login
        self.logtime = time_string_to_hours(logtime)
        self.alert = self.get_alert()

    def __str__(self):
        return f'{self.login} {self.logtime} {self.alert}'

    def __eq__(self, other):
        return self.login == other.login

    def get_alert(self):
        if self.logtime <= 10:
            return "Convocation"
        elif 10 < self.logtime <= 20:
            return "Critique"
        elif 20 < self.logtime <= 35:
            return "Attention"
        else:
            return "Good"   

def parse_file_csv(file):
    students = []
    with open(file, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader, None)
        for row in reader:
            login = row[0]
            logtime = None
            for value in reversed(row[1:]):
                if value:
                    logtime = value
                    break
            if logtime is not None and logtime != 'Absent' and login:
                student = Student(login, logtime)
                students.append(student)
    return students

def write_file(alert_students):
    with open('result.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Login", "Logtime", "Alert"])
        for student in alert_students:
            writer.writerow([student.login, student.logtime, student.alert])

def logtime(args):
    students = parse_file_csv(args.filename)
    write_file(students)
