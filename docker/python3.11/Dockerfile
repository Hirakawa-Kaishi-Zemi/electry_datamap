# Python 3.11イメージを使用
FROM python:3.11

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係のリストを作業ディレクトリにコピー
COPY ./requirements.txt /app/requirements.txt

# 依存関係のインストール
RUN pip install -U pip setuptools && pip install --no-cache-dir -r requirements.txt

# ポートを公開
EXPOSE 8050

# アプリケーションを実行
CMD [ "python", "electry_map.py" ]
