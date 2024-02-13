import glob
import pandas as pd
import os
import csv
import openpyxl
pd.options.display.max_rows = None
pd.options.display.max_columns = None


#電力会社ごとにファイル名と行数削除、不必要な削除列の変更をしながら実行する

os.chdir("/tokyo_jukyu/")
os.makedirs("/tokyo_jukyu/new", exist_ok=True)
csv_files = glob.glob('*.csv')

for csv_file in csv_files:
    with open(csv_file,"r", encoding="shift_jis", newline="",errors="" ) as f: # errors="","shift_jis",UTF-8
        lst = csv.reader(f, delimiter=",")
        df1 = pd.DataFrame(lst)
    

#4行目まで削除
        df = df1.drop([i for i in range(0,3)], axis=0)#delete col

#太陽光予測、風力予測、他を削除
        df2 = df.drop([9,11,12,13,14],axis=1)


#行番号の直し
        df3 = df2.reset_index(drop=True) #Renumber

        
        os.chdir("//tokyo_jukyu/new")
#データの書き出し
        df3.to_csv("new"+csv_file, index=False, header=False) #file save
        os.chdir("/tokyo_jukyu")
