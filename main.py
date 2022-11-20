import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
from pynput import keyboard


def main():
    path = 'Training_images'
    images = []
    classNames = []
    nameList = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
    print("\nInput 's' to stop")
    cap = cv2.VideoCapture(0)
    flag = True
    while flag:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name, nameList)
        cv2.imshow('Project', img)
        cv2.waitKey(1)


def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name, nameList):
    with open('Attendance_File\Attendance.csv', 'r+') as f:
        myDataList = f.readlines()

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n   {name}  -->   {dtString}')
                nameList.append(name)


def Print():
    cont = open("Attendance_File\Attendance.csv", "r")
    p = cont.read()
    print(p)


def cp():
    _ = os.system('cls')
    time.sleep(2)
    exis = os.path.isfile("Password_File\psd.txt")
    if exis:
        tf = open("Password_File\psd.txt", "r")
        key = tf.read()

        op = input("\nEnter old password --> ")
        newp = input("\nEnter new password --> ")
        nnewp = input("\nRe-emter new password --> ")
        if op == key:
            if newp == nnewp:
                wnp = open("Password_File\psd.txt", "w")
                wnp.write(newp)
                print('''Password changed successfully!!''')
                time.sleep(2)
            else:
                print('''Error : Re-conform new password!! ''')
                time.sleep(2)
                cp()
        else:
            print('''Error : Re-conform old password!! ''')
            time.sleep(2)
            cp()


def authencate(key1):
    password = input('\n      Enter Password --> ')

    if password == key1:
        _ = os.system('cls')
        time.sleep(1)
        print("AUTHENCATED!!\n")
        print('''************************************************************************************
                                Hello User!!
************************************************************************************''')
        ex = 1
        while ex == 1:
            print("\nMENU:-\n")
            print('''            1. Start Attendance
            2. Print Attendance
            3. Change Password
            4. Exit Application''')
            r = input('\nYour Responec --> ')

            if r == "1":
                main()
            elif r == "2":
                Print()
            elif r == "3":
                cp()
            elif r == "4":

                print("\nThankyou For Using My System")
                time.sleep(2)
                _ = os.system('cls')
                time.sleep(1)
                print("\n\nBYE!!")
                time.sleep(2)
                ex = 0
            else:
                print("Invalid Input ")

    else:
        print('\nWrong Password Entered!!')


exists1 = os.path.isfile("Password_File\psd.txt")
if exists1:
    tf = open("Password_File\psd.txt", "r")
    key = tf.read()
    print('''************************************************************************************
                  Welcome To Face Recognition Summer Project!!
************************************************************************************''')

if key == '':
    new = input('''\nUsing it for the first tikme!!
                        
Make a new Password --> ''')
    tf = open("TrainingImageLabel\psd.txt", "w")
    tf.write(new)
    print('Done!')
else:
    authencate(key)
