
import json
import os

STUDENT_FILE = "data/students.json"

def load_students():
    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_students(data):
    with open(STUDENT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def register(username, password):
    students = load_students()
    if username in students:
        return False
    students[username] = {"password": password}
    save_students(students)
    return True

def login(username, password):
    students = load_students()
    return username in students and students[username]["password"] == password
