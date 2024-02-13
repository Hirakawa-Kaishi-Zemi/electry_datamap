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
        time.sleep(3)  #ページが完全にロードされるまで待機
        
        #ダウンロードリンクを取得してクリック
        download_link = driver.find_element("css selector", css_selector)
        download_link.click()

        time.sleep(3) 

    finally:
        driver.quit()
        print("CSVファイルをダウンロードしました。")

if __name__ == "__main__":
    url = "https://www.yonden.co.jp/nw/denkiyoho/download.html" #四国電力でんき予報url
    css_selector = "#contents > dl > dd:nth-child(2) > a" #欲しいデータのCSSセレクター ※1年ごとに新しいファイルになる
    download_path = "/organaize_data/sikoku_download"

    download_csv(url, css_selector, download_path)

#contents > dl > dd:nth-child(2) > a
    