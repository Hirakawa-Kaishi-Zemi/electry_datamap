import os
from datetime import datetime, timedelta

def find_missing_dates(folder_path, date_format='%Y%m%d'):
    all_dates = set()

    # フォルダ内のファイル名から後ろから8文字を切り取り、日付を抽出
    for filename in os.listdir(folder_path):
        try:
            file_name_without_extension, _ = os.path.splitext(filename)
            last_eight_characters = file_name_without_extension[-8:]
            date_str = datetime.strptime(last_eight_characters, date_format).strftime('%Y-%m-%d')
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            all_dates.add(date_obj)
        except (ValueError, IndexError):
            pass

    # フォルダ内のファイル名で最小および最大の日付を取得
    min_date = min(all_dates)
    max_date = max(all_dates)

    # 抜けている日付を見つける
    missing_dates = [min_date + timedelta(days=i) for i in range((max_date - min_date).days) if (min_date + timedelta(days=i)) not in all_dates]

    return missing_dates

def main():
    folder_path = '/kyushu'  # フォルダのパスを指定
    missing_dates = find_missing_dates(folder_path)

    if missing_dates:
        print("Missing dates:")
        for date in missing_dates:
            print(date.strftime('%Y-%m-%d'))
    else:
        print("No missing dates found in the folder.")

if __name__ == "__main__":
    main()
