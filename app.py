# app.py
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import datetime # Firestore のタイムスタンプ用
import streamlit as st
from google.cloud import storage
from google.cloud.exceptions import NotFound # オブジェクトが見つからない場合のエラー処理用
import os
import uuid # 一意なファイル名生成のため

# タイムゾーン変換用 (必要に応じて)
try:
    # Python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:
    # Python 3.8以前 (pytz をインストールした場合)
    try:
        import pytz
        ZoneInfo = pytz.timezone # pytz を ZoneInfo として使うための簡易的な対応
    except ImportError:
        ZoneInfo = None # タイムゾーン処理不可

# --- 設定 ---
# Google Cloud プロジェクト ID を環境変数から取得（推奨）
# または直接記述（テスト目的）
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id") # デフォルトを設定
BUCKET_NAME = os.getenv("BUCKET_NAME", "your-bucket")
FIRESTORE_DATABASE_ID = os.getenv("FIRESTORE_DATABASE_ID", "your-database-id")
VERTEX_AI_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1") 

# --- Vertex AI / Firestore クライアントの初期化 ---
try:
    # Vertex AI 初期化
    vertexai.init(project=PROJECT_ID, location=VERTEX_AI_LOCATION)
    # Gemini モデル選択 (例: gemini-1.5-flash)
    model = GenerativeModel("gemini-2.0-flash-001")

    # Firestore Client (次のステップで使うがここで初期化)
    from google.cloud import firestore
    db = firestore.Client(project=PROJECT_ID, database=FIRESTORE_DATABASE_ID)

except Exception as e:
    st.error(f"Vertex AI または Firestore クライアントの初期化に失敗: {e}")
    st.stop()

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
st.title("バイク判定アプリ (v0.2)")
st.header("バイク画像をアップロード")

uploaded_file = st.file_uploader("バイクの画像を選択してください...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='アップロードされた画像', use_container_width=True)
    st.write("")

    # ボタンを押したら、アップロード、Gemini解析、Firestore保存を一連で行う
    if st.button("画像をアップロードして解析"):
        gcs_uri = None
        gemini_result_text = "解析エラー"
        identified_model = "不明"
        status = "Error"
        upload_timestamp = firestore.SERVER_TIMESTAMP # Firestore サーバータイムスタンプを使用

        try:
            # 1. GCS へのアップロード
            st.info("GCS に画像をアップロード中...")
            file_extension = os.path.splitext(uploaded_file.name)[1]
            # uploaded_file.type からより正確な mime type を取得できる場合がある
            mime_type = uploaded_file.type
            destination_blob_name = f"uploads/{uuid.uuid4()}{file_extension}"
            blob = bucket.blob(destination_blob_name)

            # アップロード (一時ファイルやメモリから効率的に)
            uploaded_file.seek(0) # Streamlit UploadedFile ポインタを先頭に戻す
            blob.upload_from_file(uploaded_file, content_type=mime_type)
            gcs_uri = f"gs://{BUCKET_NAME}/{destination_blob_name}"
            st.success(f"GCS アップロード完了: {gcs_uri}")

            # 2. Gemini API で解析
            st.info("Gemini でバイクの型式を解析中...")
            image_part = Part.from_uri(gcs_uri, mime_type=mime_type)
            prompt = """
            この画像に写っているバイクのメーカー、型式名を特定してください。
            バイク以外、または型式が不明な場合は、その旨を記載してください。
            回答はメーカーと型式名のみ、または不明である旨のみを簡潔に記述してください。
            例: ヤマハ　YZF-R1, ヤマハ　VMAX, ヤマハ SR400, 不明, バイクではない
            """

            generation_config = generative_models.GenerationConfig(
                temperature=0.2, # より決定的な回答を促す
                max_output_tokens=100
            )
            safety_settings = {
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }

            response = model.generate_content(
                [image_part, prompt],
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=False, # ストリームしない場合は False
            )

            if response.candidates and response.candidates[0].content.parts:
                gemini_result_text = response.text.strip()
                # 簡単なパース（必要に応じて改善）
                if "不明" not in gemini_result_text and "ではない" not in gemini_result_text:
                     identified_model = gemini_result_text
                     status = "Success"
                else:
                     identified_model = gemini_result_text # モデルの回答をそのまま入れる
                     status = "Identification failed"
            else:
                # 理由を表示 (例: 安全性フィルターによるブロック)
                try:
                    block_reason = response.candidates[0].finish_reason
                    safety_ratings = response.candidates[0].safety_ratings
                    gemini_result_text = f"Gemini 解析失敗 (理由: {block_reason}, Safety Ratings: {safety_ratings})"
                except Exception:
                     gemini_result_text = "Gemini 解析失敗 (空の応答)"
                status = "Gemini API Error"


            st.subheader("Gemini 解析結果:")
            st.write(gemini_result_text)


        except Exception as e:
            st.error(f"処理中にエラーが発生しました: {e}")
            status = "Processing Error"
            gemini_result_text = str(e) # エラーメッセージを記録

        # --- ここからステップ 4, 5, 6 ---
        # 3. Firestore に履歴を書き込む (次のセクションで実装)
        finally: # エラーが発生しても記録を試みる
             if gcs_uri: # GCS URI がないと記録の意味がないため
                try:
                    st.info("解析履歴を Firestore に保存中...")
                    doc_ref = db.collection("bike_analyze_history").document() # コレクション名を指定
                    data_to_save = {
                        "timestamp": upload_timestamp,
                        "gcs_uri": gcs_uri,
                        "original_filename": uploaded_file.name,
                        "content_type": mime_type,
                        "gemini_model_used": "gemini-2.0-flash-001", # 使用モデルを記録
                        "gemini_result_text": gemini_result_text,
                        "identified_model": identified_model,
                        "status": status,
                         # 必要であればユーザー情報なども追加
                    }
                    doc_ref.set(data_to_save)
                    st.success(f"Firestore に履歴を保存しました (Document ID: {doc_ref.id})")
                except Exception as e:
                    st.error(f"Firestore への保存中にエラーが発生しました: {e}")

# --- 解析履歴表示セクション ---
st.divider()
st.subheader("解析履歴 (直近10件)")

try:
    history_ref = db.collection("bike_analyze_history")
    docs = history_ref.order_by(
        "timestamp", direction=firestore.Query.DESCENDING
    ).limit(10).stream()
    history_list = list(docs)

    if not history_list:
        st.info("まだ解析履歴はありません。")
    else:
        jst = ZoneInfo('Asia/Tokyo') if ZoneInfo else None # タイムゾーンオブジェクト準備

        for doc in history_list:
            history_data = doc.to_dict()

            # タイムスタンプの取得とフォーマット
            timestamp_utc = history_data.get('timestamp')
            display_time = "時刻不明"
            if timestamp_utc and jst: # jstが取得できている場合のみ変換試行
                 try:
                     timestamp_jst = timestamp_utc.astimezone(jst)
                     display_time = timestamp_jst.strftime('%Y-%m-%d %H:%M:%S %Z')
                 except Exception as time_e:
                     display_time = f"時刻フォーマットエラー: {time_e}"
            elif timestamp_utc: # タイムゾーン情報なしならUTCで表示
                 display_time = timestamp_utc.strftime('%Y-%m-%d %H:%M:%S UTC')

            expander_title = f"{display_time} - {history_data.get('original_filename', 'ファイル名不明')}"
            with st.expander(expander_title):

                # --- 画像のダウンロードと表示 ---
                gcs_uri = history_data.get('gcs_uri')
                if gcs_uri and gcs_uri.startswith("gs://"):
                    try:
                        # storage_client は GCSアップロード用に初期化されたものを使用
                        blob = storage.Blob.from_string(gcs_uri, client=storage_client)
                        # 画像データをバイトとしてダウンロード (タイムアウトを設定)
                        image_bytes = blob.download_as_bytes(timeout=60)
                        # Streamlit で画像を表示 (幅を指定)
                        st.image(image_bytes,
                                 caption=f"画像: {history_data.get('original_filename', '')}",
                                 width=300) # 表示幅を適宜調整
                    except NotFound:
                        st.warning(f"GCSから画像が見つかりませんでした: {gcs_uri}")
                    except Exception as img_e:
                        st.warning(f"GCSからの画像の読み込み/表示中にエラー: {img_e}")
                elif gcs_uri:
                     st.warning(f"無効なGCS URIです: {gcs_uri}")
                # --- 画像表示終了 ---

                # その他の情報を表示
                st.text(f"ステータス: {history_data.get('status', 'N/A')}")
                st.text(f"判定された型式: {history_data.get('identified_model', 'N/A')}")
                st.text(f"Gemini 結果詳細: {history_data.get('gemini_result_text', 'N/A')}")
                gcs_link = history_data.get('gcs_uri', '#')
                # GCS URI リンクも引き続き表示
                st.markdown(f"GCS URI: [{gcs_link}]({gcs_link.replace('gs://', 'https://storage.cloud.google.com/')})")
                st.text(f"コンテンツタイプ: {history_data.get('content_type', 'N/A')}")
                st.text(f"使用モデル: {history_data.get('gemini_model_used', 'N/A')}")
                st.text(f"Firestore Doc ID: {doc.id}")

except Exception as e:
    st.error(f"履歴の読み込み中にエラーが発生しました: {e}")
    st.exception(e) # 詳細なエラー情報をログや画面に出力