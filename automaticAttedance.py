import os
import cv2
import csv
import pandas as pd
import datetime
import time
from threading import Thread
import static as static_path

haarcasecade_path = static_path.HAARCASECASE_PATH
trainimagelabel_path = static_path.TRAINIMAGELABEL_PATH
trainimage_path = static_path.TRAINIMAGE_PATH
studentdetail_path = static_path.STUDENTDETAIL_PATH
attendance_path = static_path.ATTENDANCE_PATH
global MSG
MSG = ""


def writeIFile(FILE_PATH, row, fieldnames, header, Mode):
    with open(FILE_PATH, Mode) as file:
        writer = csv.DictWriter(file, delimiter=',', fieldnames=fieldnames)
        # writer = csv.writer(file, delimiter=',')
        if header:
            writer.writeheader()
        writer.writerow(row)
        file.close()


def Make_Attendance(attendance, filename, text_to_speech):
    global MSG
    for i in range(0, len(attendance)):
        try:
            enroll = attendance.loc[i]["Enrollment"]
            name = attendance.loc[i]["Name"]
            depart = attendance.loc[i]["Department"]
            FILE_PATH = os.path.join(attendance_path, depart)
            FILE_PATH = os.path.join(FILE_PATH, filename)

            row = {"Enrollment": enroll,
                   "Name": name,
                   "Attendance": 1
                   }
            fieldnames = ["Enrollment", "Name", "Attendance"]
            try:
                csv_read = pd.read_csv(FILE_PATH)

                if len(csv_read.loc[csv_read["Enrollment"] == enroll]) > 0:
                    MSG = name+" your attendance already filled"
                else:
                    th = Thread(target=writeIFile, daemon=True, args=(FILE_PATH, row, fieldnames, False, 'a'))
                    th.start()
                    th.join()
                    MSG = "Attendance Filled Successfully "+name
            except Exception as e:
                print(f"error is: {e}")
                th = Thread(target=writeIFile, daemon=True, args=(FILE_PATH, row, fieldnames, True, 'w'))
                th.start()
                th.join()
                MSG = "Attendance Filled Successfully Of "+name
        except:
            pass
        finally:
            text_to_speech(MSG)

    # for choose subject and fill attendance


def AllEmployeeDetection(text_to_speech):
    now = time.time()
    future = now + 20

    try:
        global MSG, make_attendance

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(trainimagelabel_path)
        except:
            e = "Model not found,please train model"
            text_to_speech(e)
            return

        facecasCade = cv2.CascadeClassifier(haarcasecade_path)
        df = pd.read_csv(studentdetail_path)
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ["Enrollment", "Name", "Department"]
        attendance = pd.DataFrame(columns=col_names)
        while True:
            ___, im = cam.read()
            im = cv2.flip(im, 1)
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = facecasCade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                global Id
                Id, conf = recognizer.predict(gray[y: y + h, x: x + w])
                if conf < 70:
                    # print(conf)
                    global aa
                    global date
                    global timeStamp

                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                    aa = df.loc[df["Enrollment"] == Id]["Name"].values[0]
                    depart = df.loc[df["Enrollment"] == Id]["Depart"].values[0]
                    global tt
                    tt = str(Id) + "-" + aa

                    attendance.loc[len(attendance)] = [
                        Id,
                        aa,
                        depart
                    ]
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                    cv2.putText(
                        im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                    )

                else:
                    Id = "Unknown"
                    tt = str(Id)
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                    cv2.putText(
                        im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                    )

            attendance = attendance.drop_duplicates(
                ["Enrollment"], keep="first"
            )
            if time.time() > future:
                break

            cv2.imshow("Filling Attendance...", im)
            key = cv2.waitKey(30) & 0xFF
            if key == 27:
                break

        ts = time.time()

        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

        fileName = (
                date
                + ".csv"
        )

        attendance = attendance.drop_duplicates(["Enrollment"], keep="first")

        # print(f"aa is: {aa}")
        # print(f"depart is: {depart}")
        print(f"attendance is: {attendance}")

        make_attendance = Thread(target=Make_Attendance,
                                 args=(attendance, fileName, text_to_speech,))
        make_attendance.start()
    except Exception as e:
        global MSG
        print(f"error is: \n{e}")
        MSG = "No Face found for attendance"
        text_to_speech(MSG)
    finally:
        cam.release()
        cv2.destroyAllWindows()
        make_attendance.join()


def subjectChoose(text_to_speech):
    th = Thread(target=AllEmployeeDetection, daemon=True, args=(text_to_speech,))
    th.start()
