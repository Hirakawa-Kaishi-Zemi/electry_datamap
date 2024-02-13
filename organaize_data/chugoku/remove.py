import csv

def remove_last_column(input_csv, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            if row:
                # 最後の要素を削除
                del row[-1]
                writer.writerow(row)

# 使用例
input_csv_file = 'chugoku-2021.csv'  # 入力ファイル名
output_csv_file = '2chugoku-2021.csv'  # 出力ファイル名

remove_last_column(input_csv_file, output_csv_file)
