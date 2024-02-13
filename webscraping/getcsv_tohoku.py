import requests
import os

def download_csv(url, download_path):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = os.path.join(download_path, "juyo_2019_tohoku.csv") #csvのファイル名の指定
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print("CSVファイルをダウンロードしました。")
    else:
        print("ダウンロードに失敗しました。")

if __name__ == "__main__":
    url = "https://setsuden.nw.tohoku-epco.co.jp/common/demand/juyo_2022_tohoku.csv" #2022の部分を年に変更（2021.2020etc）
    download_path = "/organaize_data/tohoku_download"  #ダウンロードファイルを保存するディレクトリのパスを指定

    download_csv(url, download_path)


#https://setsuden.nw.tohoku-epco.co.jp/download.html 東北電力HP
