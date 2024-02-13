#データ読み込み
import pandas as pd
import csv
import openpyxl
pd.options.display.max_rows = None
pd.options.display.max_columns = None

df=pd.read_csv("/chubu/allchubu.csv")

df=df.drop([i for i in range(24,40349,25) ], axis=0)#delete col

#df.head(28)

#行番号の直し
df2 = df.reset_index(drop=True) #Renumber

#データの書き出し
df2.to_csv('/allcsv/chubu.csv', index=False) #file save
