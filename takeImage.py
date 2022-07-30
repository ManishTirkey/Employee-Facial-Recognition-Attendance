from threading import Thread
import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time
import static as static_path
from Clean_Files import Make_atten_file_clean

global MSG
MSG = ""


def Detect_Face(cam, detector, path, Name, Enrollment, sampleNum):
    while True:
        ret, img = cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            p = x + w
            q = y + h
            cv2.rectangle(img, (x, y), (p, q), (255, 0, 0), 2)
            sampleNum = sampleNum + 1

            cv2.imwrite(
                f"{path}\ "
                + Name
                + "_"
                + Enrollment
                + "_"
                + str(sampleNum)
                + ".jpg",
                gray[y: q, x: p],
            )

            cv2.imshow("Frame", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        elif sampleNum > 400:
            break
    cam.release()
    cv2.destroyAllWindows()


# take Image of user
def TakeImage__(l1, l2, depart, haarcasecade_path, trainimage_path):
    try:
        global MSG
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(haarcasecade_path)
        Enrollment = l1
        Name = l2
        # sampleNum = 0
        directory = Enrollment + "_" + Name
        path = os.path.join(trainimage_path, directory)
        os.mkdir(path)

        face_thread = Thread(target = Detect_Face, daemon = True, args = (cam, detector, path, Name, Enrollment, 0))
        face_thread.start()
        face_thread.join()

        row = [Enrollment, Name, depart]
        with open(static_path.STUDENTDETAIL_PATH, "a") as csvFile:
            writer = csv.writer(csvFile, delimiter = ",")
            writer.writerow(row)
            csvFile.close()
        MSG = "Images Saved of " + Name
    except FileExistsError as F:
        MSG = "Data already exists of " + Name
    except Exception as e:
        print(f"error is : {e}")
    finally:
        Make_atten_file_clean(static_path.STUDENTDETAIL_PATH)


def check_thread(thread, msg, speech, root):
    if thread.is_alive():
        msg.config(text = "Image Taking")
        root.after(1, lambda: check_thread(thread, msg, speech, root))
    else:
        msg.configure(text = MSG)
        speech(MSG)


def TakeImage(root, l1, l2, depart, haarcasecade_path, trainimage_path, message, text_to_speech):
    th = Thread(target = TakeImage__, daemon = True,
                args = (l1, l2, depart, haarcasecade_path, trainimage_path))
    th.start()
    root.after(1, lambda: check_thread(th, message, text_to_speech, root))
