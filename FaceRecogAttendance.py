from tkinter import *
from tkinter import ttk
from tkinter import messagebox as m_box
from threading import Thread

import pandas as pd
import pyttsx3
from PIL import ImageTk, Image
import static as path
import os
##### file importing
import automaticAttedance
import show_attendance
import takeImage
import trainImage
from Clean_Files import Make_atten_file_clean

haarcasecade_path = path.HAARCASECASE_PATH
trainimagelabel_path = path.TRAINIMAGELABEL_PATH
trainimage_path = path.TRAINIMAGE_PATH
studentdetail_path = path.STUDENTDETAIL_PATH
attendance_path = path.ATTENDANCE_PATH

emp_details_path = os.path.join(os.getcwd(), path.STUDENTDETAIL_PATH)


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background = "black")
    sc1.resizable(0, 0)
    Label(sc1, text = "Enrollment & Name required!!!", fg = "yellow",
          bg = "black", font = ("times", 20, " bold ")).pack()

    Button(sc1, text = "OK", command = del_sc1, fg = "yellow", bg = "black", width = 9,
           height = 1, activebackground = "Red", font = ("times", 20, " bold ")).place(x = 110, y = 50)

    sc1.mainloop()


def TakeImageUI():
    ImageUI = Toplevel()
    ImageUI.title("Take Employee Image..")
    ImageUI.geometry("680x380")
    ImageUI.iconbitmap(r"UI_Image/face.ico")
    ImageUI.lift(root)
    bg = "#E5E7E9"
    ImageUI.configure(background = bg)

    # wrapper_frame
    wrapper_frame = Frame(ImageUI)
    wrapper_frame.config(bg = bg)
    wrapper_frame.pack(fill = BOTH, expand = True)

    titl = Label(wrapper_frame, text = "Register Your Face",
                 bg = "#C39BD3", fg = "#000000", font = ("Terminal", 30))
    titl.pack(side = TOP, fill = X)

    # title_frame
    title_frame = Frame(wrapper_frame)
    title_frame.config(bg = bg)
    title_frame.pack(fill = BOTH, expand = True)

    a = Label(title_frame, text = "Enter The Details", bg = "black",
              fg = "#E5E7E9", bd = 10, font = ("Comic Sans MS", 24))
    a.pack(side = TOP, fill = X)

    # info_frame
    info_frame = Frame(title_frame)
    info_frame.config(bg = "#E5E7E9")
    info_frame.pack(side = BOTTOM, fill = BOTH, expand = True)
    info_font = ("Comic Sans MS", 12)

    lbl1 = Label(info_frame, text = "Enrollment No", font = info_font)
    lbl1.config(bg = bg)
    lbl1.grid(row = 0, column = 0, sticky = W, padx = (100, 30), pady = (10, 0))

    all_emp = len(pd.read_csv(emp_details_path)) + 1
    txt1 = Label(info_frame, text = f"Your Enrollment no. is: {all_emp}", font = info_font, bd = 0, width = 25,
                 anchor = W)
    # txt1 = Entry(info_frame, validate="key", font=info_font, bd=0, width=25)
    # txt1.focus()
    # txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")
    txt1.grid(row = 0, column = 1, sticky = W, ipady = 4)
    txt1.config(bg = "#ffffff")

    # name
    lbl2 = Label(info_frame, text = "Name", font = info_font)
    lbl2.config(bg = bg)
    lbl2.grid(row = 1, column = 0, sticky = W, padx = (100, 30), pady = 10)

    txt2 = Entry(info_frame, font = info_font, bd = 0, width = 25)
    txt2.grid(row = 1, column = 1, sticky = W, ipady = 4)

    lblD = Label(info_frame, text = "Department Name", font = info_font)
    lblD.config(bg = bg)
    lblD.grid(row = 2, column = 0, sticky = W, padx = (100, 30), pady = 10)

    c_box = ttk.Combobox(info_frame, state = "readonly", font = info_font)
    c_box['values'] = path.DEPARTMENT_NAME
    c_box.current(0)
    c_box.grid(row = 2, column = 1, sticky = W)

    lbl3 = Label(info_frame, text = "Notification", font = info_font)
    lbl3.config(bg = bg)
    lbl3.grid(row = 3, column = 0, sticky = W, padx = (100, 30), pady = 10)

    message = Label(info_frame, text = "", font = info_font)
    message.config(bg = bg)
    message.grid(row = 3, column = 1, sticky = W)

    # btn_frame
    btn_frame = Frame(wrapper_frame)
    btn_frame.pack(side = BOTTOM, fill = X)

    def take_image():
        l1 = str(all_emp)
        l2 = txt2.get()
        l2 = l2.upper()
        depart = c_box.get()

        data = pd.read_csv(path.STUDENTDETAIL_PATH)
        data = data[data["Enrollment"] == int(l1)]
        length = len(data)

        if l2 == "" or len(l2) == 0:
            m = "please enter your name First"
            message.config(text = m)
            text_to_speech(m)
            ImageUI.after(2500, lambda: message.config(text = ""))

        elif length > 0:
            m = f"hey \"{l2}\" Use different Enrollment ID"
            message.config(text = m)
            text_to_speech(m)
            ImageUI.after(2500, lambda: message.config(text = ""))
        else:
            takeImage.TakeImage(ImageUI, l1, l2, depart, haarcasecade_path,
                                trainimage_path, message, text_to_speech)
            txt1.config(text = "")
            txt2.delete(0, END)

    takeImg = Button(btn_frame, text = "Take Image", width = 15, command = take_image, font = ("Tahoma", 12, "bold"))
    takeImg.pack(side = LEFT, padx = (100, 0), pady = 15, ipady = 4)

    def train_image():
        trainImage.TrainImage(ImageUI, haarcasecade_path, trainimage_path,
                              trainimagelabel_path, message, text_to_speech, )

    # train Image function call

    trainImg = Button(btn_frame, text = "Train Image", width = 14, command = train_image, font = ("Tahoma", 12, "bold"))
    trainImg.pack(side = RIGHT, padx = (0, 150), pady = 15, ipady = 4)

    ImageUI.mainloop()


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


root = Tk()
root.title("Face Recognition Attendance System")
root.geometry("1280x720+0+0")
root.wm_iconbitmap(r"UI_Image/face.ico")
root.minsize(1280, 720)
root.config(background = "#000000")
bg = "#c6c6c6"

text = "Welcome to FaceRecognition System"
title = Label(root, text = text)
title.pack(side = TOP, fill = X, pady = (25, 0), ipady = 15)
title.config(fg = "#F2F3F4", bg = "#000000", font = "terminal 18 underline")

background_image_open = Image.open("UI_Image/bg1.jpg")
bg_img = background_image_open.resize((1366, 768))
background_image = ImageTk.PhotoImage(bg_img)
canvas = Canvas(root, bd = 0, highlightthickness = 0)
canvas.pack(side = BOTTOM, fill = BOTH, expand = True)
canvas.config(bg = "#000000")
canvas.create_image(-250, -100, image = background_image, anchor = "nw")

# exit_frame
exit_frame = Frame(root)
exit_frame.pack(side = BOTTOM, expand = True, fill = BOTH)
exit_frame.config(bg = bg)
canvas.create_window(350, 100, anchor = "nw", window = exit_frame)

# card_frame
card_frame = Frame(exit_frame)
card_frame.pack(side = LEFT, fill = BOTH, expand = True)
card_frame.config(bg = bg)

# card-1
card_frame1 = Frame(card_frame)
card_frame1.grid(row = 0, column = 0, padx = 15)
card_frame1.config(bg = bg)

reg_image = Image.open("UI_Image/register.png")
reg_img = ImageTk.PhotoImage(reg_image)
imageLabel1 = Label(card_frame1, image = reg_img)
imageLabel1.grid(row = 0, column = 0, padx = 10, pady = 10)

regBtn = Button(card_frame1, command = TakeImageUI, text = "Register", font = ("verdana 12"), height = 2, width = 20)
regBtn.grid(row = 1, column = 0, pady = (20, 30))

# card-2
card_frame2 = Frame(card_frame)
card_frame2.grid(row = 0, column = 1, padx = 15)
card_frame2.config(bg = bg)

verify_image = Image.open("UI_Image/verifyy.png")
verify_img = ImageTk.PhotoImage(verify_image)
imageLabel2 = Label(card_frame2, image = verify_img)
imageLabel2.grid(row = 0, column = 0, padx = 10, pady = 10)

takeAtten = Button(card_frame2, command = automatic_attedance, text = "Take Attendance", font = ("verdana 12"),
                   height = 2,
                   width = 20)
takeAtten.grid(row = 1, column = 0, pady = (20, 30))

# card-3
card_frame3 = Frame(card_frame)
card_frame3.grid(row = 0, column = 2, padx = 15)
card_frame3.config(bg = bg)

veiw_image = Image.open("UI_Image/attendance.png")
veiw_image = ImageTk.PhotoImage(veiw_image)
imageLabel3 = Label(card_frame3, image = veiw_image)
imageLabel3.grid(row = 0, column = 0, padx = 10, pady = 10)


def thread_call_view_atten():
    th = Thread(target = show_attendance.Attendance_ui, daemon = True)
    th.start()


View_btn = Button(card_frame3, command = thread_call_view_atten, text = "View Attendance", font = ("verdana 12"),
                  height = 2,
                  width = 20)
View_btn.grid(row = 1, column = 0, pady = (20, 30))


def Destroy(master):
    Exit = m_box.askyesno("EXIT", "Are you Sure You Want to Exit!")
    if Exit:
        master.destroy()


def Enter(btn):
    btn.config(bg = "#58D68D", fg = "#fff")


def Lv(btn):
    btn.config(bg = "#fff", fg = "#000000")


root.protocol("WM_DELETE_WINDOW", lambda: Destroy(root))
regBtn.bind("<Enter>", lambda event: Enter(regBtn))
regBtn.bind("<Leave>", lambda event: Lv(regBtn))
takeAtten.bind("<Enter>", lambda event: Enter(takeAtten))
takeAtten.bind("<Leave>", lambda event: Lv(takeAtten))

root.mainloop()
