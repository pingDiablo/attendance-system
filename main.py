import cv2
import os
import pickle
import cvzone
import numpy as np

import face_recognition
import numpy as np
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage




cred = credentials.Certificate(r"C:\Users\kusha\Desktop\attendance system\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL" :"https://face-recognition-attenda-5a0b4-default-rtdb.firebaseio.com/",
    "storageBucket": "face-recognition-attenda-5a0b4.appspot.com"
}
                              )
bucket = storage.bucket()

cap = cv2.VideoCapture("http://192.168.1.11:8080//video")
cap.set(3, 640)
cap.set(4, 480)

imgbackground  = cv2.imread("resources/background.png")

#importing modes and backgrounds for various images
folderModePath = "resources\modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
#print(len(imgModeList))
#load the encoding file

print("loading Encode File.......")
file  = open("EncodeFile.p",'rb')
encodeListKnowsWithIds = pickle.load(file)
file.close()
encodeListKnows, studentsIds = encodeListKnowsWithIds
print("Encode file loaded Successfully")
modeType = 0
counter = 0
id = -1
imgStudent = []
#print(studentsIds)


while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)



    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgbackground[162:162 + 480, 55:55 + 640] = img
    imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnows, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnows, encodeFace)
            print(faceDis)
            print(matches)


            matchIndex = np.argmin(faceDis)
            print("Match Index", matchIndex)



            if matches[matchIndex]:
                print("Known Face Detected")
                print(studentsIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55 + x1 , 162+y1, x2-x1 , y2-y1
                imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0 )
                id = studentsIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgbackground, "loading " , (275, 400))
                    cv2.imshow("Face Attendance", imgbackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
        if counter != 0:

            if counter == 1:
                #get data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                #get img of the student from storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent = cv2.imdecode(array , cv2.COLOR_BGRA2BGR)

                #update date of attendance:

                dateTimeObject = datetime.strptime(studentInfo['Last_attendance_time'],
                                                   '%Y-%m-%d %H:%M:%S')
                secondsElapsed = (datetime.now() - dateTimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed>30:
                #update attendance
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('Last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                else:
                    modeType = 3
                    counter = 0
                    imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            if modeType != 3:

                if 10<counter<20:
                    modeType = 2
                imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:

                    cv2.putText(imgbackground, str(studentInfo["total_attendance"]), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(studentInfo["major"]), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(studentInfo["Standing"]), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgbackground, str(studentInfo["Semester"]), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgbackground, str(studentInfo["starting_year"]), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w,h), _ = cv2.getTextSize(studentInfo["name"], cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414-w)//2
                    cv2.putText(imgbackground, str(studentInfo["name"]), (808+offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)


                    imgbackground[175:175+216 , 909:909 + 216] = imgStudent


                counter+=1


                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []

                    imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    else:

        modeType = 0
        counter = 0
        imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    cv2.imshow("Face Attendance", imgbackground)
    cv2.waitKey(1)











