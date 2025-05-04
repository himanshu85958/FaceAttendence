# Face Recognition Attendance System 🧑‍🏫🧠🎥

This is a Python-based GUI application for managing attendance using facial recognition. It supports role-based login (Admin/Student), secure user management, attendance marking through a webcam, and an easy-to-use modern Tkinter interface.



## 🔧 Features

- 🔐 **Login System**: Secure role-based access (Admin or Student).
- 🧍‍♂️ **Face Registration**: Captures 30 face samples using OpenCV.
- 🤖 **Face Recognition**: Uses `face_recognition` for accurate detection.
- 📅 **Attendance Tracking**: Marks attendance with date and time.
- 📊 **View Records**:
  - Admins can view all records.
  - Students can view their own records.
- 👤 **Admin Controls**:
  - Add new users (with face data).
  - Delete users and their face datasets.
- 📦 **Data Storage**:
  - User credentials in `students.json`
  - Face data in `data/dataset/`
  - Attendance logs in `attendance.csv`

---

## 📁 Project Structure

face-recognition-attendance/
│
├── face_attendance_system.py # Main app
├── data/
│ ├── students.json # User database
│ ├── attendance.csv # Attendance log
│ └── dataset/ # Face data per user
├── haarcascade_frontalface_default.xml
├── icon.ico # App icon (optional)
└── README.md

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone [https://github.com/himanshu85958/FaceAttendence.git]
cd face-recognition-attendance
2. Install dependencies
Create a virtual environment (recommended):

bash
Copy
Edit
python -m venv face_env
face_env\Scripts\activate  # For Windows
Install required packages:

bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is missing, install manually:

bash
Copy
Edit
pip install opencv-python face_recognition pillow
3. Run the app
bash
Copy
Edit
python face_attendance_system.py
📸 Face Registration Workflow
Admin adds a user with a role (admin or student).

The webcam opens and captures 30 grayscale images of the user's face.

Images are saved in data/dataset/<username>/.

🛠 Requirements
Python 3.7+

Webcam

Libraries:

opencv-python

face_recognition

Pillow

tkinter (built-in)

🖼 Screenshots
Login Page	Admin Panel	Face Capture

Add your own screenshots in the screenshots/ folder and update these links.

🔐 Default Admin (Optional)
You can add an initial admin manually to data/students.json:

json
Copy
Edit
{
  "adminuser": {
    "password": "admin123",
    "role": "admin"
  }
}
📌 Notes
Ensure haarcascade_frontalface_default.xml is present for face detection.

Attendance is logged with real-time timestamps.

Works offline – no internet needed after setup.

📃 License
MIT License. Feel free to use and modify.

👨‍💻 Author
Your Name – @himanshugautam
