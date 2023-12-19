# 最新のMySQLイメージを使用
FROM mysql:latest

# 環境変数の設定
# ただしdocker-compose.ymlの設定値が優先されることに注意すること
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=electry_map
ENV MYSQL_USER=guest
ENV MYSQL_PASSWORD=password

# ポートを公開
EXPOSE 3306
