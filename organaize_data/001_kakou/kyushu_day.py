import glob
import pandas as pd
import os
import csv
import openpyxl
pd.options.display.max_rows = None
pd.options.display.max_columns = None

os.chdir("/kyushu_download")
#os.makedirs("2023_tokyo", exist_ok=True)
csv_files = glob.glob('*.csv')

for csv_file in csv_files:
    with open(csv_file,"r", encoding="shift_jis", newline="",errors="" ) as f: 
        lst = csv.reader(f, delimiter=",")
        df1 = pd.DataFrame(lst)
    

#12行目まで削除
        df = df1.drop([i for i in range(0,13)], axis=0)#delete col

#予測値と使用率、供給力想定値を削除
        df2 = df.drop([3,4,5,6],axis=1)

#最大使用率以降の行を削除(38行目から)
        df3 = df2.drop([i for i in range(39,344)], axis=0)#delete col

        df3 = df3.drop(df3.index[-1])#最後の行削除

#行番号の直し
        df3 = df3.reset_index(drop=True) #Renumber

        
        os.chdir("/kyushu/")
#データの書き出し
        df3.to_csv("new"+csv_file, index=False, header=False) #file save
        os.chdir("/kyushu_download")
