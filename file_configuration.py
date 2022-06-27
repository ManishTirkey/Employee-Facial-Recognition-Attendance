import static as static_file_path
import os
import csv
import pandas as pd


def create_folders():
    for folder in static_file_path.STATIC_FOLDER:
        try:
            os.mkdir(folder)
        except Exception as e:
            pass

    parent_dir = static_file_path.STATIC_FOLDER[0]
    for folder in static_file_path.DEPARTMENT_NAME:
        try:
            dir = os.path.join(parent_dir, folder)
            os.mkdir(dir)
        except:
            pass


def create_files():
    for file in static_file_path.STATIC_FILE:
        try:
            with open(file, 'a+') as file:
                file.close()
        except:
            print("file exists")


def CSV_file():
    field_names = ["Enrollment", "Name", "Depart"]
    try:
        data = pd.read_csv(static_file_path.STATIC_FILE[0])

    except pd.errors.EmptyDataError:
        with open(static_file_path.STATIC_FILE[0], "a") as file:
            writer = csv.DictWriter(file, delimiter=',', fieldnames=field_names)
            writer.writeheader()
            file.close()


create_folders()
create_files()
CSV_file()
