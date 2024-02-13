import pandas as pd
import csv

# エンコーディングを適切に設定してください
with open("/sikoku_download/juyo_shikoku_2023.csv", "r", encoding="shift_jis", errors="", newline="" ) as f:
    lst = csv.reader(f, delimiter=",")
    df1 = pd.DataFrame(lst)

# 列ヘッダーが存在する場合、以下のように読み込むこともできます
# df1 = pd.read_csv("./chugoku_download/juyo-2023.csv", encoding="shift_jis")

# 1,2行目を削除
df2 = df1.drop([0, 1], axis=0)
#4列目を削除
df3 = df2.drop([3],axis=1)

# 行番号を振り直す
df3 = df3.reset_index(drop=True)

# ファイルを新しい名前で保存（保存場所を指定してください）
df3.to_csv('sikoku-2023.csv', index=False, header=False)
