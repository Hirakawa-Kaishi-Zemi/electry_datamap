from selenium import webdriver
import time

def download_csv(url,select_year,select_month,select_day, download_path):
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
        time.sleep(0.5)  #ページが完全にロードされるまで待機
        
        #日付入力フィールドを特定してそれぞれ年月日を入力
        date_input = driver.find_element("css selector", "#year")
        date_input.send_keys(select_year)

        date_input = driver.find_element("css selector", "#month")
        date_input.send_keys(select_month)

        date_input = driver.find_element("css selector", "#day")
        date_input.send_keys(select_day)


        #ダウンロードをクリック
        download_link = driver.find_element("css selector", "#download-form > form > ul > li:nth-child(1) > a > img")
        download_link.click()
        time.sleep(0.2) 

    finally:
        driver.quit()
        print("CSVファイルをダウンロードしました。")


if __name__ == "__main__":
    url = "https://www.rikuden.co.jp/nw/denki-yoho/#download" #北陸電力でんき予報url
    download_path = "/organaize_data/hokuriku_download"
    select_year = "2023"  # 目的の日付に置き換える
    select_month = "9"
    select_day = "18"

    download_csv(url,select_year,select_month,select_day, download_path)

