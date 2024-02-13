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
        time.sleep(0.2)  #ページが完全にロードされるまで待機
        
        #ダウンロードリンクを取得してクリック
        download_link = driver.find_element("css selector", css_selector)
        download_link.click()

        time.sleep(0.5) 

    finally:
        driver.quit()
        print("CSVファイルをダウンロードしました。")

def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

if __name__ == "__main__":
    url = "https://www.tepco.co.jp/forecast/html/download_year-j.html" #東京電力でんき予報url
    css_selector = "#content-forecast > ul:nth-child(6) > li:nth-child(2) > a" #(2)が先月の分、(1)は現在の月
    download_path = "/organaize_data/tokyo_download"
    zip_file_name = "202307_power_usage.zip" #ファイル名 年月202307_power_usage.zip(7月) 

    download_csv(url, css_selector, download_path)

    zip_file_path = os.path.join(download_path, zip_file_name)
    unzip_file(zip_file_path, download_path)

