import glob
import pandas as pd
import os
import csv
import openpyxl
pd.options.display.max_rows = None
pd.options.display.max_columns = None

os.chdir("/hokkaido_download")
csv_files = glob.glob('*.csv')

for csv_file in csv_files:
    with open(csv_file,"r", encoding="shift_jis", newline="",errors="" ) as f: # errors="","shift_jis",UTF-8
        lst = csv.reader(f, delimiter=",")
        df1 = pd.DataFrame(lst)
    

#12行目まで削除
        df = df1.drop([i for i in range(0,7)], axis=0)#delete col

#予測値と使用率、供給力想定値を削除
        df2 = df.drop([3,4],axis=1)

#最大使用率以降の行を削除(38行目から)
        df3 = df2.drop([i for i in range(33,331)], axis=0)#delete col

        df3 = df3.drop(df3.index[-1])#最後の行削除

#行番号の直し
        df3 = df3.reset_index(drop=True) #Renumber

        
        os.chdir("/hokkaido/")
#データの書き出し
        df3.to_csv("new"+csv_file, index=False, header=False) #file save
        os.chdir("/hokkaido_download")
