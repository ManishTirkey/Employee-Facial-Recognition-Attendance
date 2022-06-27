import os
import cv2
import os

import numpy as np
from PIL import Image
from threading import Thread


# Train Image
def Train_Image(haarcasecade_path, trainimage_path, trainimagelabel_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Id = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Id))
    recognizer.save(trainimagelabel_path)


def getImagesAndLables(path):
    # imagePath = [os.path.join(path, f) for d in os.listdir(path) for f in d]
    newdir = [os.path.join(path, d) for d in os.listdir(path)]
    imagePath = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i])
    ]
    faces = []
    Ids = []
    for imagePath in imagePath:
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")
        Id = int(os.path.split(imagePath)[-1].split("_")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def check_thread(thread, msg, speech, root):
    if thread.is_alive():
        msg.config(text="Training Image....")
        root.after(1, lambda: check_thread(thread, msg, speech, root))
    else:
        res = "Image Trained successfully"  # +",".join(str(f) for f in Id)
        msg.configure(text=res)
        speech(res)


def TrainImage(root, haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    th = Thread(target=Train_Image,
                args=(haarcasecade_path, trainimage_path, trainimagelabel_path,))
    th.start()
    root.after(4, lambda: check_thread(th, message, text_to_speech, root))
