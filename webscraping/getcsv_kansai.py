from selenium import webdriver
import time
import zipfile
import os

def download_csv(url,target_text,download_path):
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
        
        #要素のテキスト内容を含むリンクを特定してクリック
        links = driver.find_elements("css selector", "a")
        for link in links:
            if target_text in link.text:
                link.click()
                break

        time.sleep(5) 

    finally:
        driver.quit()
        print("CSVファイルをダウンロードしました。")


def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


if __name__ == "__main__":
    url = "https://www.kansai-td.co.jp/denkiyoho/download/index.html" #関西電力でんき予報url
    target_text = "2023年6月"  # クリックしたいリンクのテキストに置き換える　**
    download_path = "/organaize_data/kansai_download"
    zip_file_name = "202306_jisseki.zip" #ファイル名 年月202306_jisseki.zip(6月) 

    download_csv(url, target_text, download_path)

    zip_file_path = os.path.join(download_path, zip_file_name)
    unzip_file(zip_file_path, download_path)

