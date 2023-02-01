import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL" :"https://face-recognition-attenda-5a0b4-default-rtdb.firebaseio.com/"
}
                              )


ref = db.reference("Students")


data = {
    "23221" :
        {
            "name" : "Kushagra",
            "major": "AIML",
            "starting_year": 2020,
            "total_attendance": 6,
            "Standing" :"Good",
            "Semester": 6,
            "Last_attendance_time": "2023-01-25 08:55:12"

        },
    "23291" :
        {
            "name" : "Obama",
            "major": "Politics",
            "starting_year": 2011,
            "total_attendance": 15,
            "Standing" :"Good",
            "Semester": 8,
            "Last_attendance_time": "2014-07-21 05:12:16"

        },
    "23416" :
        {
            "name" : "Tony Stark",
            "major": "Suits",
            "starting_year": 2000,
            "total_attendance": 40,
            "Standing" :"Bad",
            "Semester": 8,
            "Last_attendance_time": "2005-03-25 12:11:52"

        },
    "23851":
        {
            "name" : "Spiderman",
            "major": "Biology",
            "starting_year": 2019,
            "total_attendance": 8,
            "Standing" :"Good",
            "Semester": 8,
            "Last_attendance_time": "2023-01-25 08:55:12"

        },
    "23991" :
        {
            "name" : "Biden",
            "major": "Politics",
            "starting_year": 2001,
            "total_attendance": 44,
            "Standing" :"Bad",
            "Semester": 8,
            "Last_attendance_time": "2001-05-25 16:55:12"

        },
"23209" :
        {
            "name" : "Ananya Jha",
            "major": "Politics",
            "starting_year": 2001,
            "total_attendance": 44,
            "Standing" :"Bad",
            "Semester": 8,
            "Last_attendance_time": "2001-05-25 16:55:12"




        }
}
for key, value in data.items():
    ref.child(key).set(value)
