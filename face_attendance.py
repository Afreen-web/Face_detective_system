from markAttendance import markAttendance
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

# 1. Load student images and create encodings
path = 'images'
images = []
student_names = []
my_list = os.listdir(path)

for cl in my_list:
    cur_img = cv2.imread(f'{path}/{cl}')
    images.append(cur_img)
    student_names.append(os.path.splitext(cl)[0])  # Get name without extension

def encode_faces(images):
    encoded_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded = face_recognition.face_encodings(img)[0]
        encoded_list.append(encoded)
    return encoded_list

encoded_faces = encode_faces(images)

# 2. Create attendance CSV
def mark_attendance(name):
    try:
        df = pd.read_csv('attendance.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Name', 'Time'])
    
    if name not in df['Name'].values:
        now = datetime.now()
        time_string = now.strftime('%H:%M:%S')
        df = pd.concat([df, pd.DataFrame({'Name':[name],'Time':[time_string]})], ignore_index=True)
        df.to_csv('attendance.csv', index=False)

# 3. Capture video and recognize faces
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_small = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
    img_rgb = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    faces_cur_frame = face_recognition.face_locations(img_rgb)
    encodes_cur_frame = face_recognition.face_encodings(img_rgb, faces_cur_frame)

    for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
        matches = face_recognition.compare_faces(encoded_faces, encode_face)
        face_dist = face_recognition.face_distance(encoded_faces, encode_face)
        match_index = np.argmin(face_dist)

        if matches[match_index]:
            name = student_names[match_index].upper()
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4  # Scale back
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(img, name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
