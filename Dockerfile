# Dockerfile

# ベースイメージを選択 (Python 3.11 のスリム版を使用)
FROM python:3.11-slim

# 環境変数 PORT を設定 (Cloud Run はこのポートでリッスンすることを期待する)
ENV PORT 8080
# Python の出力をバッファリングしない (ログがすぐに見えるように)
ENV PYTHONUNBUFFERED TRUE

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピーしてインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# コンテナがリッスンするポートを公開
EXPOSE ${PORT}

# アプリケーションを実行するコマンド
# Cloud Run では 0.0.0.0 でリッスンし、PORT 環境変数を尊重する必要がある
# WebSocket の問題を回避するため --server.enableCORS false を含める
CMD streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0 --server.enableCORS=false