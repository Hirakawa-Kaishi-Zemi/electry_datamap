#データ読み込み
import pandas as pd
from datetime import datetime as dt
pd.options.display.max_rows = None
pd.options.display.max_columns = None

df=pd.read_csv("/dataset/time_kwh.csv")

df['DATETIME'] = (df['DATE'] + " "+ df['TIME'])

df.to_csv('/dataset/time_kwh1.csv',index=False)
