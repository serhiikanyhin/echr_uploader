import time
import sqlite3


def export_exel(df):
    timestamp = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    df.to_excel("export/echr_data " + timestamp + ".xlsx", sheet_name='data')
