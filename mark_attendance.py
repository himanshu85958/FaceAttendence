
import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import csv

def mark_attendance(name):
    with open("data/attendance.csv", "a", newline="") as f:
        writer = csv.writer(f)
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([name, dt_string])

def recognize_face():
    known_encodings = []
    known_names = []

    for user_folder in os.listdir("data/dataset"):
        user_path = os.path.join("data/dataset", user_folder)
        for img_name in os.listdir(user_path):
            img_path = os.path.join(user_path, img_name)
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_encodings.append(encoding[0])
                known_names.append(user_folder)

    cam = cv2.VideoCapture(0)
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
