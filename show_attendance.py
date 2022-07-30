import pandas as pd
from glob import glob
import os
import csv
from tkinter import *
from tkinter import ttk
import static
from threading import Thread
import pandas as pd


def Enter(btn, bg = "#fff", fg = "#000000"):
    btn.config(bg = bg, fg = fg)


def Lv(btn, bg = "#fff", fg = "#000000"):
    btn.config(bg = bg, fg = fg)


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
    root.minsize(500, 300)
    root.maxsize(500, 300)
    root.config(bg = "#ECF0F1")

    font = ("Comic Sans MS", 12)

    label_1 = Label(root, text = "Choose your Department", font = font)
    label_1.grid(row = 0, column = 0, sticky = W, pady = (10, 0), padx = (25, 30))
    label_1.config(bg = "#ECF0F1")

    c_box1 = ttk.Combobox(root, state = "readonly", font = font)
    c_box1['values'] = static.DEPARTMENT_NAME
    c_box1.current(0)
    c_box1.grid(row = 0, column = 1, sticky = W)

    label_2 = Label(root, text = "Attendance of Date", font = font)
    label_2.grid(row = 1, column = 0, sticky = W, pady = (10, 0), padx = (25, 30))
    label_2.config(bg = "#ECF0F1")

    c_box2 = ttk.Combobox(root, state = "readonly", font = font)
    # c_box.current(0)
    c_box2.grid(row = 1, column = 1, sticky = W)

    def Attendance_cal():
        try:
            data = pd.read_csv(static.STUDENTDETAIL_PATH)
            path = os.getcwd()
            path = os.path.join(path, static.ATTENDANCE_PATH)
            depart = c_box1.get()
            path = os.path.join(path, depart)
            file = c_box2.get()

            if file != "no file":
                path = os.path.join(path, file)
                path = path + ".csv"
                print(f"path is: {path} ")
                atten_data = pd.read_csv(path)
                print(f"\natten data is :\n{atten_data} \nlength is: {len(atten_data)}")

                print(f"\ndetails is: \n{data}")

                depart_persons = data.loc[data["Depart"] == depart]
                print(f"\ndepart_persons: \n{depart_persons}")

                presences_emp = int(len(atten_data))
                total_depart_emp = int(len(depart_persons))

                if presences_emp == total_depart_emp:
                    show_presence.config(text="All employee peresents")
                    show_Absent.config(text="no one Absent")
                elif total_depart_emp > presences_emp:
                    show_presence.config(text = f"{presences_emp} Present out of {total_depart_emp}")
                    show_Absent.config(text = f"{(total_depart_emp-presences_emp)} Absent")

            else:
                path = ""
                print("empty path")
                show_presence.config(text = "-")
                show_Absent.config(text = "-")
        except:
            pass

    def Start_Attendance():
        th = Thread(target=Attendance_cal)
        th.start()

    presence_label = Label(root, text = "Presence", font = font)
    presence_label.grid(row = 2, column = 0, sticky = W, pady = (10, 0), padx = (25, 30))
    show_presence = Label(root, text = "hello", font = font, anchor = W)
    show_presence.grid(row = 2, column = 1, sticky = W, ipady = 4)
    show_presence.config(bg = "#ffffff", width = 25)

    Absent_label = Label(root, text = "Absent", font = font)
    Absent_label.grid(row = 3, column = 0, sticky = W, pady = (10, 0), padx = (25, 30))
    show_Absent = Label(root, text = "hello", font = font, anchor = W)
    show_Absent.grid(row = 3, column = 1, sticky = W, ipady = 4)
    show_Absent.config(bg = "#ffffff", width = 25)

    def Csv_files_find():
        Start_Attendance()
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

    def Start_file(path = None):
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
            th = Thread(target = Start_file, daemon = True, args = (path,))
            th.start()

    show_btn = Button(root, command = show_Atten, text = "Show Attendance", width = 16, font = ("verdana", 12, "bold"))
    show_btn.grid(row = 4, column = 1, sticky = W, ipady = 4, pady = (30, 0))
    show_btn.config(bg = "#fff", fg = "#58D68D", bd = 0)

    show_btn.bind("<Enter>", lambda event: Enter(show_btn, bg = "#58D68D", fg = "#fff"))
    show_btn.bind("<Leave>", lambda event: Lv(show_btn, bg = "#fff", fg = "#58D68D"))
    c_box1.bind("<<ComboboxSelected>>", lambda event: Csv_files_find())
    c_box2.bind("<<ComboboxSelected>>", lambda event: Start_Attendance())
    Csv_files_find()
    root.mainloop()
