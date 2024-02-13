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
        time.sleep(0.2)  #ページが完全にロードされるまで待機
        
        #ダウンロードリンクを取得してクリック
        download_link = driver.find_element("css selector", css_selector)
        download_link.click()

        time.sleep(0.1) 

    finally:
        driver.quit()
        print("CSVファイルをダウンロードしました。")

if __name__ == "__main__":
    url = "https://www.okiden.co.jp/denki2/dl/2023/202309.html" #沖縄電力でんき予報url　2023は年度を表示/202306の部分でひと月を表示(202305なら5月分)
    css_selector = "#content > div.container > div.section-box > div > ul > li:nth-child(1) > span > a" #(1)が0630、２が0629、日付の新しいものが上
    download_path = "/organaize_data/okinawa_download"
#content > div.container > div.section-box > div > ul > li:nth-child(1) > span > a
    
    download_csv(url, css_selector, download_path)
