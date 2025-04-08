# app.py
import streamlit as st
from google.cloud import storage
import os
import uuid # 一意なファイル名生成のため

# --- 設定 ---
# Google Cloud プロジェクト ID を環境変数から取得（推奨）
# または直接記述（テスト目的）
# PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
PROJECT_ID = "gossy-workstations" # あなたのプロジェクト ID に置き換えてください
# GCS バケット名を設定
BUCKET_NAME = "gossy-gemini-handson" # 作成したバケット名に置き換えてください

# --- GCS クライアントの初期化 ---
# Cloud Workstations や Cloud Run (サービスアカウント指定時) では通常、
# 自動的に認証情報が検出されます。
# ローカルで gcloud auth application-default login を実行した場合も同様です。
try:
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
except Exception as e:
    st.error(f"GCS クライアントの初期化に失敗しました: {e}")
    st.stop() # エラーが発生したらアプリを停止

# --- Streamlit アプリケーション ---
st.title("ヤマハバイク判定アプリ (v0.2)")
st.header("バイク画像をアップロード")

uploaded_file = st.file_uploader("ヤマハバイクの画像を選択してください...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされたファイルの内容を表示（任意）
    st.image(uploaded_file, caption='アップロードされた画像', use_column_width=True)
    st.write("")

    # GCS にアップロードするボタン
    if st.button("画像を GCS にアップロード"):
        try:
            # ファイル名を一意にする (例: UUID + 元の拡張子)
            file_extension = os.path.splitext(uploaded_file.name)[1]
            destination_blob_name = f"uploads/{uuid.uuid4()}{file_extension}"

            # GCS にファイルをアップロード
            blob = bucket.blob(destination_blob_name)

            # Streamlit の UploadedFile はファイルライクオブジェクトなのでそのまま渡せる
            blob.upload_from_file(uploaded_file)

            st.success(f"画像が GCS にアップロードされました: gs://{BUCKET_NAME}/{destination_blob_name}")
            st.session_state.gcs_file_path = f"gs://{BUCKET_NAME}/{destination_blob_name}" # 後続ステップのためにパスを保持

        except Exception as e:
            st.error(f"GCS へのアップロード中にエラーが発生しました: {e}")