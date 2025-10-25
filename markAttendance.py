import csv
from datetime import datetime
import os

def markAttendance(name):
    file_path = 'attendance.csv'

    # Create the file with headers if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Time", "Date"])

    with open(file_path, 'r+', newline='') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.strip().split(',')
            nameList.append(entry[0].lower())  # convert to lowercase for comparison

        if name.lower() not in nameList:
            now = datetime.now()
            timeString = now.strftime('%H:%M:%S')
            dateString = now.strftime('%d/%m/%Y')
            writer = csv.writer(f)
            writer.writerow([name, timeString, dateString])
            print(f"✅ Attendance marked for {name} at {timeString} on {dateString}")
            print("Saving to:",os.path.abspath(file_path))
