import pandas as pd
import csv

# エンコーディングを適切に設定してください
with open("/tohoku_download/juyo_2023_tohoku.csv", "r", encoding="shift_jis", errors="", newline="" ) as f:
    lst = csv.reader(f, delimiter=",")
    df1 = pd.DataFrame(lst)

# 列ヘッダーが存在する場合、以下のように読み込むこともできます
# df1 = pd.read_csv("./chugoku_download/juyo-2023.csv", encoding="shift_jis")

# 1,2行目を削除
df2 = df1.drop([0], axis=0)


# 行番号を振り直す
df3 = df2.reset_index(drop=True)

# ファイルを新しい名前で保存（保存場所を指定してください）
df3.to_csv('tohoku-2023.csv', index=False, header=False)
