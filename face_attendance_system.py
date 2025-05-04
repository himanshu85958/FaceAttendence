import os
import json
import cv2
import csv
import shutil
import face_recognition
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk  # Import ttk for modern widgets
from PIL import Image, ImageTk  # Import PIL for image handling

# ========== Paths ========== 
STUDENT_FILE = "data/students.json"
ATTENDANCE_FILE = "data/attendance.csv"
DATASET_DIR = "data/dataset"
os.makedirs(DATASET_DIR, exist_ok=True)

# ========== Globals ========== 
logged_in_user = None
user_role = None

# Define color scheme
BACKGROUND_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4CAF50"
BUTTON_HOVER_COLOR = "#45a049"
TEXT_COLOR = "#333"

# ========== Utilities ========== 
def load_students():
    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_students(data):
    with open(STUDENT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def mark_attendance(name):
    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([name, dt_string])

def recognize_face():
    known_encodings = []
    known_names = []

    for user_folder in os.listdir(DATASET_DIR):
        user_path = os.path.join(DATASET_DIR, user_folder)
        for img_name in os.listdir(user_path):
            img_path = os.path.join(user_path, img_name)
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_encodings.append(encoding[0])
                known_names.append(user_folder)

    cam = cv2.VideoCapture(0)
    messagebox.showinfo("Info", "Press ESC to stop scanning")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, faces)

        for enc, loc in zip(encodings, faces):
            matches = face_recognition.compare_faces(known_encodings, enc)
            name = "Unknown"
            if True in matches:
                index = matches.index(True)
                name = known_names[index]
                mark_attendance(name)

            top, right, bottom, left = loc
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) == 27:
            break
    cam.release()
    cv2.destroyAllWindows()

def capture_face(username):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    dataset_path = os.path.join(DATASET_DIR, username)
    os.makedirs(dataset_path, exist_ok=True)

    count = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            cv2.imwrite(f"{dataset_path}/{count}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow("Register Face", frame)

        if cv2.waitKey(1) == 27 or count >= 30:
            break

    cam.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Info", "Face data captured.")

def view_attendance(user_only=False):
    if not os.path.exists(ATTENDANCE_FILE):
        messagebox.showinfo("Attendance", "No attendance records yet.")
        return
    records = []
    with open(ATTENDANCE_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if user_only and row[0] != logged_in_user:
                continue
            records.append(f"{row[0]} | {row[1]}")
    if records:
        messagebox.showinfo("Attendance Records", "\n".join(records))
    else:
        messagebox.showinfo("Attendance Records", "No records found.")

# ========== Admin Functions ========== 
def register_and_capture_user():
    username = simpledialog.askstring("New User", "Enter Username:")
    password = simpledialog.askstring("New User", "Enter Password:", show='*')
    role = simpledialog.askstring("New User", "Enter Role (admin/student):")

    if not username or not password or not role:
        return
    role = role.lower()
    if role not in ['admin', 'student']:
        messagebox.showerror("Error", "Role must be 'admin' or 'student'.")
        return

    students = load_students()
    if username in students:
        messagebox.showerror("Error", "Username already exists.")
        return

    students[username] = {"password": password, "role": role}
    save_students(students)
    capture_face(username)

def delete_user():
    username = simpledialog.askstring("Delete User", "Enter Username to Delete:")
    students = load_students()
    if username not in students:
        messagebox.showerror("Error", "User  not found.")
        return

    del students[username]
    save_students(students)
    dataset_path = os.path.join(DATASET_DIR, username)
    if os.path.exists(dataset_path):
        shutil.rmtree(dataset_path)
    messagebox.showinfo("Success", f"User  '{username}' deleted.")

# ========== GUI Menus ========== 
def logout(root, frame):
    global logged_in_user, user_role
    logged_in_user = None
    user_role = None
    frame.destroy()
    show_login_menu(root)

def show_login_menu(root):
    login_frame = ttk.Frame(root, padding="20")
    login_frame.pack(fill="both", expand=True)
    root.configure(bg=BACKGROUND_COLOR)

    ttk.Label(login_frame, text="Username:", background=BACKGROUND_COLOR).pack()
    username_entry = ttk.Entry(login_frame)
    username_entry.pack(fill="x", pady=10)

    ttk.Label(login_frame, text="Password:", background=BACKGROUND_COLOR).pack()
    password_entry = ttk.Entry(login_frame, show="*")
    password_entry.pack(fill="x", pady=10)

    def attempt_login():
        global logged_in_user, user_role
        username = username_entry.get()
        password = password_entry.get()
        students = load_students()
        if username in students and students[username]["password"] == password:
            logged_in_user = username
            user_role = students[username].get("role", "student")
            login_frame.destroy()
            if user_role == "admin":
                show_admin_menu(root)
            else:
                show_student_menu(root)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    ttk.Button(login_frame, text="Login", command=attempt_login).pack(pady=5)
    ttk.Button(login_frame, text="Exit", command=root.quit).pack(pady=5)

def show_student_menu(root):
    student_frame = ttk.Frame(root, padding="20")
    student_frame.pack(fill="both", expand=True)

    ttk.Label(student_frame, text=f"Welcome, {logged_in_user} (Student)", font=("Arial", 16), background=BACKGROUND_COLOR).pack(pady=10)
    ttk.Button(student_frame, text="Mark Attendance", command=recognize_face).pack(pady=5)
    ttk.Button(student_frame, text="View My Attendance", command=lambda: view_attendance(user_only=True)).pack(pady=5)
    ttk.Button(student_frame, text="Logout", command=lambda: logout(root, student_frame)).pack(pady=5)
    ttk.Button(student_frame, text="Exit", command=root.quit).pack(pady=5)

def show_admin_menu(root):
    admin_frame = ttk.Frame(root, padding="20")
    admin_frame.pack(fill="both", expand=True)

    ttk.Label(admin_frame, text=f"Welcome, {logged_in_user} (Admin)", font=("Arial", 16), background=BACKGROUND_COLOR).pack(pady=10)
    ttk.Button(admin_frame, text="Add New User (with Face)", command=register_and_capture_user).pack(pady=5)
    ttk.Button(admin_frame, text="Delete User", command=delete_user).pack(pady=5)
    ttk.Button(admin_frame, text="View All Attendance", command=lambda: view_attendance(user_only=False)).pack(pady=5)

    # Logout button
    def logout_admin():
        logout(root, admin_frame)

    ttk.Button(admin_frame, text="Logout", command=logout_admin).pack(pady=5)

    # Exit button
    ttk.Button(admin_frame, text="Exit", command=root.quit).pack(pady=5)

# ========== Run App ========== 
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Face Recognition Attendance System")
    root.geometry("800x600")  # Start with a larger size
    root.attributes('-fullscreen', True)  # Fullscreen on start
    root.iconbitmap(r"C:\Users\HIMANSHU\OneDrive\Desktop\p2\icon.ico")  # Full path

    show_login_menu(root)
    root.mainloop()
