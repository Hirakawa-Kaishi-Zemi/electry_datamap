#東京電力　年間ファイル」
import pandas as pd
import csv
import openpyxl

pd.options.display.max_rows = None
pd.options.display.max_columns = None

with open("tokyo/juyo-2019.csv", "r", encoding="shift_jis", errors="", newline="" ) as f:
    lst = csv.reader(f, delimiter=",")
    df1 = pd.DataFrame(lst)

#1,2行目削除
df2 = df1.drop([0,1], axis=0)#delete col


#行番号の直し
df3 = df2.reset_index(drop=True) #Renumber


df3.to_csv('./tokyo2019.csv', index=False, header=False) #file save