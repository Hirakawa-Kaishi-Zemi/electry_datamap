import pandas as pd
import csv

# エンコーディングを適切に設定
with open("/chugoku_download/juyo-2023.csv", "r", encoding="shift_jis", errors="", newline="" ) as f:
    lst = csv.reader(f, delimiter=",")
    df1 = pd.DataFrame(lst)

# 1,2行目を削除
df2 = df1.drop([0, 1], axis=0)

# 行番号を振り直す
df3 = df2.reset_index(drop=True)

# ファイルを新しい名前で保存
df3.to_csv('chugoku-2023.csv', index=False, header=False)
