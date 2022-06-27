import csv

import pandas as pd
import os
import csv as CSV

path = f"./attendance"
filename = "test.csv"
filename = os.path.join(path, filename)

# col_names = ["Enrollment", "Name"]
# attendance = pd.DataFrame(columns=col_names)
# date = "1-1-2021"
#
# # def Make_attendance(ID, name, date, filename):
# #     csv = pd.read_csv(filename)
# #     persons = csv.loc[csv["Enrollment"] == ID]
# #     index_Range = csv.index
# #
# #     if len(persons) > 0:
# #         enrollment = [enroll for enroll in persons["Enrollment"].values]
# #         print(f"length is: {len(persons)}")
# #         print(f"enrollment is: {enrollment}")
# #         print(f"persons are: {persons}")
# #         # csv[date] = 0
# #         print(csv)
# #         # csv.to_csv(filename)
# #         # print(name)
# #         list = index_Range[csv["Enrollment"] == ID]
# #         index_list = list.tolist()
# #         print(csv)
# # Make_attendance(12, "manish", "2-2-2021", filename=filename)
#
#
# attendance.loc[len(attendance)] = [
#     12, "manish"
# ]
# # attendance.to_csv(filename, index=False)
# print(attendance)
#
# attendance.loc[len(attendance)] = [13, "manisha"]
# # attendance.to_csv(filename, index=False)
# print(attendance)
#
# attendance.loc[len(attendance)] = [14, "manishaa"]
# # attendance.to_csv(filename, index=False)
# print(attendance)
#
#
# print("for loop ")
# for atten in attendance:
#     print(atten, end=", ")
#
# print("\nafter for loop")
#
# csv = pd.read_csv(filename)
# for i in range(0, len(attendance)):
#     name = attendance.loc[i]["Name"]
#     enroll = attendance.loc[i]["Enrollment"]
#     atten = 1
#     row = [enroll, name, atten]
#     # print(name, enroll, atten)
#     # print(row)
#
#     if len(csv.loc[csv["Enrollment"] == enroll]):
#         print("attendance already filled")
#     else:
#         # print("failed")
#         with open(filename, 'a') as file:
#             writter = CSV.writer(file)
#             writter.writerow(row)
#             file.close()
#
#
#
# # print(csv)
# # h = csv.loc[csv["Enrollment"] == 12]
# # print(f"\nh is: \n{len(h)}")

text = "my name is manish tirkey"
print(text.upper())
