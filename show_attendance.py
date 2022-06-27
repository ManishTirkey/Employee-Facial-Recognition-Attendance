import pandas as pd
from glob import glob
import os
import tkinter
import csv
from tkinter import *
from tkinter import ttk
import static
from threading import Thread


def Enter(btn, bg="#fff", fg="#000000"):
    btn.config(bg=bg, fg=fg)


def Lv(btn, bg="#fff", fg="#000000"):
    btn.config(bg=bg, fg=fg)


def filter_extensions(files):
    csv_file = []
    cwd = os.getcwd()
    for file in files:
        if file.endswith(".csv"):
            file_name = file.split(".")[0]
            csv_file.append(file_name)
    return csv_file


def Attendance_ui():
    root = Tk()
    root.title("Attendance")
    root.geometry("500x200")
    root.iconbitmap("UI_Image/face.ico")
    root.minsize(500, 200)
    root.maxsize(500, 200)
    root.config(bg="#ECF0F1")

    font = ("Comic Sans MS", 12)

    label_1 = Label(root, text="Choose your Department", font=font)
    label_1.grid(row=0, column=0, sticky=W, pady=(10, 0), padx=(25, 30))
    label_1.config(bg="#ECF0F1")

    c_box1 = ttk.Combobox(root, state="readonly", font=font)
    c_box1['values'] = static.DEPARTMENT_NAME
    c_box1.current(0)
    c_box1.grid(row=0, column=1, sticky=W)

    label_2 = Label(root, text="Attendance of Date", font=font)
    label_2.grid(row=1, column=0, sticky=W, pady=(10, 0), padx=(25, 30))
    label_2.config(bg="#ECF0F1")

    c_box2 = ttk.Combobox(root, state="readonly", font=font)
    # c_box.current(0)
    c_box2.grid(row=1, column=1, sticky=W)

    def Csv_files_find():
        depart = c_box1.get()
        try:
            cwd = os.getcwd()
            path = os.path.join(cwd, static.ATTENDANCE_PATH)
            path = os.path.join(path, depart)
            files = os.listdir(path)
            if files:
                csv_files = filter_extensions(files)
            else:
                csv_files = ["no file"]
        except FileNotFoundError:
            csv_files = ["no file"]

        c_box2['values'] = csv_files
        c_box2.current(0)

    def Start_file(path=None):
        if path is not None:
            os.startfile(path)

    def show_Atten():
        depart = c_box1.get()
        date = c_box2.get()
        if date != "no file":
            BASE_DIR = os.getcwd()
            path = os.path.join(BASE_DIR, static.ATTENDANCE_PATH)
            path = os.path.join(path, depart)
            path = os.path.join(path, f"{date}.csv")
            th = Thread(target=Start_file, daemon=True, args=(path,))
            th.start()
            # os.startfile(path)

    show_btn = Button(root, command=show_Atten, text="Show Attendance", width=16, font=("verdana", 12, "bold"))
    show_btn.grid(row=2, column=1, sticky=W, ipady=4, pady=(30, 0))
    show_btn.config(bg="#fff", fg="#58D68D", bd=0)

    show_btn.bind("<Enter>", lambda event: Enter(show_btn, bg="#58D68D", fg="#fff"))
    show_btn.bind("<Leave>", lambda event: Lv(show_btn, bg="#fff", fg="#58D68D"))
    c_box1.bind("<<ComboboxSelected>>", lambda event: Csv_files_find())
    Csv_files_find()
    root.mainloop()
