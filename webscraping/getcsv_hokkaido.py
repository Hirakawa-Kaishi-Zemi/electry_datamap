from selenium import webdriver
import time
import zipfile
import os

def download_csv(url,css_selector,download_path):
    #seleniumの設定
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") #ブラウザを非表示にする場合
    options.add_argument("--disable-gpu") #GPUを使用しない場合
    options.add_argument("--window-size=1920x1080") #画面サイズを指定
    options.add_argument("--lang=ja") #言語を日本語に設定
    prefs = {"download.default_directory": download_path} #ダウンロードパスを指定
    options.add_experimental_option("prefs", prefs)

    #Chromeドライバーを起動
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url) 
        time.sleep(5)  #ページが完全にロードされるまで待機
        
        #ダウンロードリンクを取得してクリック
        download_link = driver.find_element("css selector", css_selector)
        download_link.click()

        time.sleep(5) 

    finally:
        driver.quit()
        print("CSVファイルをダウンロードしました。")

def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


if __name__ == "__main__":
    url = "https://denkiyoho.hepco.co.jp/area_download.html" #北海道電力でんき予報url
    css_selector = "#l_main > div.main_inner.clear_fix > div.main_contents > div.section.mb_30 > ul:nth-child(4) > li:nth-child(2) > a" #(4)-(2)が最新
    download_path = "/organaize_data/hokkaido_download"
    zip_file_name = "202304-06_hokkaido_denkiyohou.zip" #ファイル名 年月202304-06_hokkaido_denkiyohou.zip **

    download_csv(url, css_selector, download_path)

    zip_file_path = os.path.join(download_path, zip_file_name)
    unzip_file(zip_file_path, download_path)
