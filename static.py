import os
STATIC_FOLDER = ["attendance",       # 0
                 "EmpDetails",      # 1
                 "TrainingImageLabel",  # 2
                 "TrainingImage"]      # 3

STATIC_FILE = [os.path.join(STATIC_FOLDER[1], "Emp_details.csv"),
               os.path.join(STATIC_FOLDER[2], "Trainner.yml")]

HAARCASECASE_PATH = r"haarcascade_frontalface_default.xml"
TRAINIMAGELABEL_PATH = r"TrainingImageLabel/Trainner.yml"
TRAINIMAGE_PATH = r"TrainingImage"
STUDENTDETAIL_PATH = r"EmpDetails/Emp_details.csv"
ATTENDANCE_PATH = r"attendance/"


DEPARTMENT_NAME = [
    "Science",
    "Math",
    "Space",
    "Computer"
]
