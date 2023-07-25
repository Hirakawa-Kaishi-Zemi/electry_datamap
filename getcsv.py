import time
import glob
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

############### ダウンロード機能の追加 ###############
# ダウンロードファイルの一時保存フォルダを作成(カレントディレクトリに「tmp」フォルダを作成)
tmp_dir = Path(Path.cwd(), "tmp")
tmp_dir.mkdir(exist_ok=True, parents=True)

# webdriverにオプションを追加
options = Options()
prefs = {"download.default_directory": str(tmp_dir)}
options.add_experimental_option("prefs", prefs)

# chromedriverのパスを指定
driver_path = "/Users/mibo/Downloads/chromedriver"
chrome_service = Service(executable_path=driver_path)

# 追加したオプションを設定してwebdriverを起動
driver = webdriver.Chrome(service=chrome_service, options=options)


############### ここからWebページへのアクセス処理 ###############
# e-Statsのcsvダウンロードページにアクセス
url = "https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001011777&cycle=0&tclass1=000001094741&tclass2val=0"
driver.get(url=url)