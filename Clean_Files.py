import pandas as pd
import os
import static
from threading import Thread

cwd = os.getcwd()
col_rm_list = ["unnamed"]
row_rm_list = ["nan"]
# --------------------------------------------------------------


def Get_Columns_Name(df):
    col_names = df.columns.values
    return col_names


def Remove_Row(df, Row_rm_list):
    rm_row_index_list = []
    for row_rm_name in Row_rm_list:
        col_names = Get_Columns_Name(df)
        for col in col_names:
            series = df[col]
            for index, val in enumerate(series):
                if row_rm_name in str(val).lower():
                    if index not in rm_row_index_list:
                        rm_row_index_list.append(index)
    if len(rm_row_index_list) > 0:
        df.drop(rm_row_index_list, axis=0, inplace=True)


def Remove_Col(df, columns_rm_list):
    for col_rm_name in columns_rm_list:
        col_names = Get_Columns_Name(df)
        rm_col = [val for val in col_names if col_rm_name in str(val).lower()]
        for col in rm_col:
            df.drop([col], axis = 1, inplace = True)


def Main(filename):
    empp = pd.read_csv(filename, index_col = False)
    Remove_Col(empp, col_rm_list)
    Remove_Row(empp, row_rm_list)
    empp.to_csv(filename, index = False)


def Make_atten_file_clean(path):
    th = Thread(target=Main, daemon=True, args=(path,))
    th.start()
