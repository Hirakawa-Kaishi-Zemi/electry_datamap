from selenium import webdriver
import time


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
        time.sleep(1)  #ページが完全にロードされるまで待機
        
        #ダウンロードリンクを取得してクリック
        download_link = driver.find_element("css selector", css_selector)
        download_link.click()

        time.sleep(0.5) 

    finally:
        driver.quit()
        print("CSVファイルをダウンロードしました。")

if __name__ == "__main__":
    url = "https://www.kyuden.co.jp/td_power_usages/history202401.html" #九州電力でんき予報url 202306の部分でひと月を表示(202305なら5分)
    css_selector = "#main-contents > table > tbody > tr:nth-child(2) > td:nth-child(8)" #(2)が0601、3が02、4が03
    download_path = "/organaize_data/kyushu_download"
#main-contents > table > tbody > tr:nth-child(2) > td:nth-child(8) > a
    
    download_csv(url, css_selector, download_path)
