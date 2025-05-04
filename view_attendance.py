
import csv

def show_attendance():
    with open("data/attendance.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print("Name:", row[0], "| Time:", row[1])
