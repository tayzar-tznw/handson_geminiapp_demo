# ハンズオン: Google Cloud で AI 画像分析 Web アプリを作ろう！ (Gemini, Cloud Run, Firestore)

**最終更新:** 2025年4月11日

このリポジトリは、Google Cloud の各種サービスを組み合わせて AI 画像分析 Web アプリケーションを構築するハンズオンワークショップのガイドです。Cloud Workstations を開発環境として使用し、Streamlit アプリを作成、Cloud Storage への画像アップロード、Gemini API での分析、Firestore への履歴保存、そして Cloud Run への直接デプロイまでをステップバイステップで学習します。(Git および CI/CD 手順は含みません)

## 目次

* [対象者](#対象者)
* [学習目標](#学習目標)
* [所要時間 (目安)](#所要時間-目安)
* [必要なもの](#必要なもの)
* [モジュール 1: 開発環境のセットアップ (Cloud Workstations)](#モジュール-1-開発環境のセットアップ-cloud-workstations)
* [モジュール 2: 基本的な Web アプリの作成 (Streamlit)](#モジュール-2-基本的な-web-アプリの作成-streamlit)
* [モジュール 3: 画像アップロード機能の追加 (Cloud Storage)](#モジュール-3-画像アップロード機能の追加-cloud-storage)
* [モジュール 4: アプリの Cloud Run へのデプロイ (ソースコードから)](#モジュール-4-アプリの-cloud-run-へのデプロイ-ソースコードから)
* [モジュール 5: AI による画像分析機能の追加 (Gemini API)](#モジュール-5-ai-による画像分析機能の追加-gemini-api)
* [モジュール 6: 分析履歴の保存 (Firestore)](#モジュール-6-分析履歴の保存-firestore)
* [モジュール 7: 履歴の表示 (Firestore & GCS 画像)](#モジュール-7-履歴の表示-firestore--gcs-画像)
* [モジュール 8: クリーンアップ (リソースの削除)](#モジュール-8-クリーンアップ-リソースの削除)
* [まとめ と 次のステップ](#まとめ-と-次のステップ)
* [参考: 必要な API と IAM ロール](#参考-必要な-api-と-iam-ロール)

## 対象者

* Google Cloud をこれから学びたい方、初学者の方
* Python の基本的な知識がある方
* Web アプリケーション開発・デプロイに興味がある方

## 学習目標

* Cloud Workstations を使ったクラウドベースの開発環境の利用方法
* Streamlit を使った簡単な Web アプリケーションの作成
* Cloud Storage へのファイルアップロード機能の実装
* `gcloud` コマンドを使った Cloud Run への直接デプロイ (ソースコードから)
* Gemini API (Vertex AI) を使った画像分析の実装
* Firestore を使った NoSQL データベースへのデータ保存と読み取り

## 所要時間 (目安)

* 1〜2 時間 

## 必要なもの

* Google Cloud プロジェクト (課金が有効になっていること)
* プロジェクト内で各種リソースを作成・管理できる権限 (オーナーまたは編集者ロール推奨)
* `gcloud` コマンドラインツールが利用可能な環境 (Cloud Workstations 内で利用)

---

## モジュール 1: 開発環境のセットアップ (Cloud Workstations)

クラウド上でコーディングできる、便利な開発環境を準備します。

1.  **API の有効化:**
    * Google Cloud Console で、使用するプロジェクトを選択します。
    * ナビゲーションメニューから [API とサービス] > [ライブラリ] を選択します。
    * 以下の API を検索し、それぞれ「有効にする」をクリックします:
        * `Cloud Workstations API`
        * `Compute Engine API` (通常デフォルトで有効)

2.  **ワークステーション構成の作成:**
    * ナビゲーションメニューから [Cloud Workstations] > [ワークステーション構成] を選択します。
    * [作成] をクリックし、指示に従って構成を作成します (名前: `dev-config`, リージョン選択など)。

3.  **ワークステーションの起動:**
    * 作成した構成 (`dev-config`) を選択し、[ワークステーション] タブで [作成] をクリックしてワークステーションを起動します (名前: `my-dev-workstation` など)。

4.  **ワークステーションへの接続:**
    * ステータスが [実行中] になったら、[起動] ボタンをクリックしてブラウザで開発環境を開きます。

---

## モジュール 2: 基本的な Web アプリの作成 (Streamlit)

シンプルな Web アプリを作成します。

1.  **必要なツールの確認とインストール:**
    * ワークステーションのターミナルを開きます (VS Code の場合: [Terminal] > [New Terminal])。
    * Python 仮想環境ツール `venv` が必要です。なければインストールします:
        ```bash
        sudo apt update
        sudo apt install python3-venv -y
        ```

2.  **プロジェクトディレクトリの作成:**
    ```bash
    mkdir image-analysis-app
    cd image-analysis-app
    ```

3.  **Python 仮想環境の作成と有効化:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # プロンプトの先頭に (venv) と表示されればOK
    ```

4.  **Streamlit のインストール:**
    ```bash
    pip install streamlit
    ```

5.  **"Hello World" アプリの作成 (`app.py`):**
    * ワークステーションのエディタ (VS Code など) で、`image-analysis-app` ディレクトリ内に `app.py` という名前のファイルを作成し、以下の内容を記述します。
    ```python
    # app.py
    import streamlit as st

    st.title("画像分析アプリ (v0.1)")
    st.header("Hello, Google Cloud!")
    st.write("Cloud Workstations で開発中！")
    ```

6.  **動作確認 (ローカル実行):**
    ```bash
    streamlit run app.py
    ```
    ターミナルに URL が表示されます。[Open in Browser] ボタンが表示されたらクリックするか、表示されたポート (通常 8501) を手動で転送設定して `localhost:8501` にアクセスします。"Hello, Google Cloud!" が表示されたら、ターミナルで `Ctrl+C` を押してアプリを停止します。

7.  **`requirements.txt` の作成:** アプリの依存ライブラリを記録します。
    ```bash
    pip freeze > requirements.txt
    ```
    (`streamlit` とその依存ライブラリが含まれていることを確認してください)

---

## モジュール 3: 画像アップロード機能の追加 (Cloud Storage)

ユーザーが画像をアップロードし、それをクラウドに保存する機能を追加します。

1.  **API の有効化:**
    * Google Cloud Console で `Cloud Storage API` を検索し、有効にします。

2.  **GCS バケットの作成:**
    * [Cloud Storage] > [バケット] で [作成] をクリックします。
    * **名前:** **世界中で一意** な名前 (例: `your-project-id-image-bucket`) を入力。 **`your-project-id-image-bucket` を実際に使うバケット名に置き換えてください。**
    * リージョン、アクセス制御 (均一)、公開アクセス禁止などを設定し、作成します。

3.  **必要なライブラリのインストール:**
    ```bash
    # (venv が有効な状態で)
    pip install google-cloud-storage
    ```

4.  **`requirements.txt` の更新:**
    ```bash
    pip freeze > requirements.txt
    ```

5.  **`app.py` の修正:** `app.py` ファイルを開き、内容を以下のように修正します。
    ```python
    # app.py の修正・追記
    import streamlit as st
    from google.cloud import storage
    import os
    import uuid

    # --- 設定 ---
    # ★★★ 次の2行をご自身のプロジェクトIDとバケット名に置き換えてください ★★★
    # ★★★ (モジュール4で環境変数から読むように変更します) ★★★
    PROJECT_ID = "your-project-id"
    BUCKET_NAME = "your-project-id-image-bucket"

    # --- GCS クライアントの初期化 ---
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
    except Exception as e:
        st.error(f"GCS クライアントの初期化に失敗しました: {e}")

    # --- Streamlit アプリケーション ---
    st.title("画像分析アプリ (v0.2)")
    st.header("画像をアップロード")

    uploaded_file = st.file_uploader("分析したい画像を選択してください...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='アップロードされた画像', use_column_width=True)
        st.write("")

        if st.button("画像を GCS にアップロード"):
            try:
                st.info("GCS に画像をアップロード中...")
                file_extension = os.path.splitext(uploaded_file.name)[1]
                mime_type = uploaded_file.type
                destination_blob_name = f"uploads/{uuid.uuid4()}{file_extension}"

                blob = bucket.blob(destination_blob_name)
                uploaded_file.seek(0)
                blob.upload_from_file(uploaded_file, content_type=mime_type)

                gcs_uri = f"gs://{BUCKET_NAME}/{destination_blob_name}"
                st.success(f"画像が GCS にアップロードされました: {gcs_uri}")

            except Exception as e:
                st.error(f"GCS へのアップロード中にエラーが発生しました: {e}")
                st.exception(e)
    ```
    **【重要】** コード中の `your-project-id` と `your-project-id-image-bucket` を、ご自身の値に**必ず置き換えてください**。

6.  **認証と権限 (Workstation ローカル実行時):**
    * GCS への書き込み権限が必要です。ターミナルで Application Default Credentials (ADC) を設定します:
        ```bash
        gcloud auth application-default login
        ```
    * ログインしたユーザーアカウントに、対象 GCS バケットへの書き込み権限 (`roles/storage.objectAdmin` または `objectCreator`) が必要です。IAM ページで確認・付与してください。

7.  **動作確認 (ローカル実行):**
    * `app.py` を保存し、`streamlit run app.py` でローカル実行します。
    * 画像をアップロードし、GCS に保存されることを確認します。

---

## モジュール 4: アプリの Cloud Run へのデプロイ (ソースコードから)

作成したアプリを、Cloud Workstations 上のソースコードから直接 Cloud Run にデプロイします。

1.  **API の有効化:**
    * Google Cloud Console で `Cloud Run Admin API` を検索し、有効にします。

2.  **`app.py` の環境変数対応:** `app.py` が `PROJECT_ID` と `BUCKET_NAME` をハードコードではなく `os.getenv()` で読み取るように修正します。(モジュール 3 で実施済み)
    ```python
    # app.py の設定部分 (再掲)
    import os # ファイル先頭で import

    # --- 設定 ---
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    BUCKET_NAME = os.getenv("BUCKET_NAME")

    # 環境変数が設定されていない場合のエラー処理 (推奨)
    if not PROJECT_ID:
        st.error("環境変数 GOOGLE_CLOUD_PROJECT が設定されていません。")
        st.stop()
    if not BUCKET_NAME:
        st.error("環境変数 BUCKET_NAME が設定されていません。")
        st.stop()

    # --- GCS クライアントの初期化 ---
    # ... (変更なし) ...
    ```
    * この修正を `app.py` に適用し、保存してください。

3.  **Cloud Run サービスアカウントへの権限付与:** Cloud Run で動作するアプリが GCS にアクセスするために権限が必要です。
    * プロジェクト番号を取得:
        ```bash
        # ★★★ $PROJECT_ID を実際のプロジェクトIDに置き換えるか、環境変数として設定 ★★★
        export PROJECT_ID="your-project-id"
        PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
        ```
    * Cloud Run が使用するサービスアカウント (デフォルト: Compute Engine default SA) に権限を付与します:
        ```bash
        # ★★★ $BUCKET_NAME を実際のバケット名に置き換えるか、環境変数として設定 ★★★
        export BUCKET_NAME="your-project-id-image-bucket"
        gcloud storage buckets add-iam-policy-binding gs://$BUCKET_NAME \
            --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
            --role="roles/storage.objectAdmin"
        ```

4.  **Cloud Run へのデプロイ (ソースコードから):**
    * ワークステーションのターミナルで、**`app.py` と `requirements.txt` があるディレクトリ (`image-analysis-app`) にいることを確認**します。
    * 以下のコマンドを実行してデプロイします:
        ```bash
        # ★★★ 値を置き換えてください ★★★
        export REGION="asia-northeast1" # デプロイするリージョン
        export SERVICE_NAME="image-analysis-service" # Cloud Run のサービス名 (任意)
        # BUCKET_NAME は上で export 済みのはず

        gcloud run deploy $SERVICE_NAME \
          --source . \
          --region=$REGION \
          --platform=managed \
          --allow-unauthenticated \
          --set-env-vars="BUCKET_NAME=$BUCKET_NAME"
        ```
    * `--source .`: カレントディレクトリのソースコードを使って Cloud Run が自動でビルド・デプロイします。
    * `--allow-unauthenticated`: 認証なしアクセスを許可します (学習用)。
    * `--set-env-vars`: アプリが必要とする環境変数を設定します。
    * デプロイには数分かかります。完了するとサービスの URL が表示されます。

5.  **デプロイの確認:**
    * 表示された URL にブラウザでアクセスし、アプリが動作することを確認します。
    * 画像をアップロードし、GCS に保存されることを確認します。

---

## モジュール 5: AI による画像分析機能の追加 (Gemini API)

アップロードされた画像を Gemini API に渡し、画像の内容を分析させます。

1.  **API の有効化:**
    * Google Cloud Console で `Vertex AI API` を検索し、有効にします。

2.  **必要なライブラリのインストール:** (Firestore も含める)
    ```bash
    # (venv が有効な状態で)
    pip install google-cloud-aiplatform google-cloud-firestore pytz # pytz はタイムゾーン用(任意)
    ```

3.  **`requirements.txt` の更新:**
    ```bash
    pip freeze > requirements.txt
    ```

4.  **IAM 権限の付与:** Cloud Run サービスアカウントに Vertex AI API 呼び出し権限を付与します。
    ```bash
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role="roles/aiplatform.user"
    ```

5.  **`app.py` の修正:** `app.py` をエディタで開き、Gemini API 呼び出しロジックを追加します。(前のモジュールで追加した Firestore クライアント初期化も含む)
    ```python
    # app.py の全体を以下のように修正・追記
    import streamlit as st
    from google.cloud import storage
    import os
    import uuid
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part, FinishReason
    import vertexai.preview.generative_models as generative_models
    import datetime
    from google.cloud import firestore
    from google.cloud.exceptions import NotFound
    try: from zoneinfo import ZoneInfo
    except ImportError:
        try: import pytz; ZoneInfo = pytz.timezone
        except ImportError: ZoneInfo = None

    # --- 設定 ---
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    VERTEX_AI_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1")

    if not PROJECT_ID or not BUCKET_NAME or not VERTEX_AI_LOCATION:
        st.error("環境変数 (GOOGLE_CLOUD_PROJECT, BUCKET_NAME, VERTEX_AI_LOCATION) が不足しています。")
        st.stop()

    # --- クライアント初期化 ---
    try:
        vertexai.init(project=PROJECT_ID, location=VERTEX_AI_LOCATION)
        model = GenerativeModel("gemini-1.5-flash-001")
        db = firestore.Client(project=PROJECT_ID)
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
    except Exception as e:
        st.error(f"クライアント初期化失敗: {e}"); st.stop()

    # --- Streamlit アプリケーション ---
    st.title("画像分析アプリ (v1.0)")
    st.write(f"Project: {PROJECT_ID}, Bucket: {BUCKET_NAME}, Vertex AI Location: {VERTEX_AI_LOCATION}")

    uploaded_file = st.file_uploader("分析したい画像を選択してください...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='アップロードされた画像', use_column_width=True)

        if st.button("画像をアップロードして解析"):
            gcs_uri, gemini_result_text, analysis_result, status = None, "解析未実行", "不明", "Pending"
            upload_timestamp = firestore.SERVER_TIMESTAMP

            with st.spinner('処理中... (1/3 GCSアップロード > 2/3 Gemini解析 > 3/3 Firestore保存)'):
                try:
                    # 1. GCS Upload
                    st.write("1/3: GCS に画像をアップロード中...")
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                    mime_type = uploaded_file.type
                    destination_blob_name = f"uploads/{uuid.uuid4()}{file_extension}"
                    blob = bucket.blob(destination_blob_name)
                    uploaded_file.seek(0)
                    blob.upload_from_file(uploaded_file, content_type=mime_type)
                    gcs_uri = f"gs://{BUCKET_NAME}/{destination_blob_name}"
                    st.write(f"GCS アップロード完了: {gcs_uri}")

                    # 2. Gemini Analysis
                    st.write("2/3: Gemini で画像を分析中...")
                    image_part = Part.from_uri(gcs_uri, mime_type=mime_type)
                    # ★★★ プロンプトを自由に調整 ★★★
                    prompt = "この画像について説明してください。画像に写っている主要なオブジェクトや状況を簡潔に記述してください。"
                    generation_config = generative_models.GenerationConfig(temperature=0.4, max_output_tokens=200)

                    response = model.generate_content(
                        [image_part, prompt], generation_config=generation_config, stream=False
                    )

                    if response.candidates and response.candidates[0].content.parts:
                        gemini_result_text = response.text.strip()
                        analysis_result = gemini_result_text; status = "Success"
                        st.write("Gemini 解析完了")
                    else:
                        gemini_result_text = "Gemini 解析失敗 (空またはブロックされた応答)"
                        try: block_reason = response.candidates[0].finish_reason; safety_ratings = response.candidates[0].safety_ratings
                        except Exception: pass
                        status = "Gemini API Error"; st.warning(gemini_result_text)

                    st.subheader("Gemini 分析結果:")
                    st.markdown(f"```\n{analysis_result}\n```")

                    # 3. Firestore Write
                    st.write("3/3: 解析履歴を Firestore に保存中...")
                    doc_ref = db.collection("image_analysis_history").document() # ★★★ コレクション名 ★★★
                    data_to_save = {
                        "timestamp": upload_timestamp, "gcs_uri": gcs_uri, "original_filename": uploaded_file.name,
                        "content_type": mime_type, "gemini_model_used": model.name, "gemini_result_text": gemini_result_text,
                        "analysis_result": analysis_result, "status": status,
                    }
                    doc_ref.set(data_to_save)
                    st.success(f"Firestore に履歴を保存しました (Doc ID: {doc_ref.id})")

                except Exception as e:
                    status = "Processing Error"; error_message = f"処理中にエラー: {str(e)}"
                    st.error(error_message); st.exception(e)
                    # エラー時の記録 (オプション)
                    # ...

    # --- 解析履歴表示セクション (次のモジュールで実装) ---
    st.divider()
    st.subheader("解析履歴 (直近10件)")
    # ... (ここに履歴表示コードが入る) ...
    ```
    * `app.py` を保存します。

6.  **再デプロイ (環境変数追加):** `VERTEX_AI_LOCATION` を追加してデプロイします。
    ```bash
    # ★★★ リージョンと言語モデル利用可能リージョンを必要に応じて変更 ★★★
    export REGION="asia-northeast1"
    export VERTEX_AI_LOCATION="us-central1"
    export SERVICE_NAME="image-analysis-service"
    export BUCKET_NAME="your-project-id-image-bucket" # 正しいバケット名を設定

    gcloud run deploy $SERVICE_NAME \
      --source . \
      --region=$REGION \
      --platform=managed \
      --allow-unauthenticated \
      --set-env-vars="BUCKET_NAME=$BUCKET_NAME,VERTEX_AI_LOCATION=$VERTEX_AI_LOCATION"
    ```
    * デプロイ後、アプリで画像分析を実行し、Gemini の結果が表示されることを確認します。

---

## モジュール 6: 分析履歴の保存 (Firestore)

Gemini の分析結果を含む処理履歴を Firestore データベースに保存します。

* **このステップの実装は、モジュール 5 の `app.py` 修正内容に既に含まれています。**

1.  **API の有効化:**
    * Google Cloud Console で `Firestore API` を検索し、有効にします。
    * 初めて Firestore を使う場合、[Firestore] ページで [データベースの作成] を行い、**Native モード** と **ロケーション** を選択します。

2.  **必要なライブラリのインストール:** (モジュール 5 で実施済み)

3.  **`requirements.txt` の更新:** (モジュール 5 で実施済み)

4.  **IAM 権限の付与:** Cloud Run サービスアカウントに Firestore への書き込み権限を付与します。
    ```bash
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role="roles/datastore.user"
    ```

5.  **`app.py` の修正:** (モジュール 5 で実施済み)
    * Firestore クライアント初期化、データ書き込みが実装されています。コレクション名は `image_analysis_history` です。

6.  **再デプロイとテスト:**
    * `gcloud run deploy ...` コマンド (モジュール 5 の最後と同じもの) で再デプロイします。
    * アプリで画像分析を実行し、成功メッセージを確認します。
    * Google Cloud Console の [Firestore] ページで `image_analysis_history` コレクションにデータが保存されていることを確認します。

---

## モジュール 7: 履歴の表示 (Firestore & GCS 画像)

Firestore に保存した履歴と、対応する画像をアプリ内に表示します。

1.  **(オプション) `pytz` のインストール:** (モジュール 5 で実施済み or 不要ならスキップ)

2.  **`app.py` の修正:** ファイル末尾の履歴表示セクション (コメントアウトされていた部分) を実装します。`app.py` をエディタで開き、以下のコードブロックをファイルの末尾に追加または修正します。
    ```python
    # app.py の修正 (ファイル末尾に追加)

    # ... (これまでのコードはそのまま) ...

    # --- 解析履歴表示セクション ---
    st.divider()
    st.subheader("解析履歴 (直近10件)")

    # タイムゾーン準備
    jst = None
    try: from zoneinfo import ZoneInfo; jst = ZoneInfo('Asia/Tokyo')
    except ImportError:
        try: import pytz; jst = pytz.timezone('Asia/Tokyo')
        except ImportError: pass

    try:
        history_ref = db.collection("image_analysis_history")
        docs = history_ref.order_by(
            "timestamp", direction=firestore.Query.DESCENDING
        ).limit(10).stream()
        history_list = list(docs)

        if not history_list:
            st.info("まだ解析履歴はありません。")
        else:
            for doc in history_list:
                history_data = doc.to_dict()

                # タイムスタンプ表示
                timestamp_utc = history_data.get('timestamp')
                display_time = "時刻不明"
                if timestamp_utc:
                    if jst:
                         try: display_time = timestamp_utc.astimezone(jst).strftime('%Y-%m-%d %H:%M:%S %Z')
                         except: display_time = "TZ変換エラー"
                    else:
                         try: display_time = timestamp_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
                         except: display_time = "時刻フォーマットエラー"

                # Expander
                expander_title = f"{display_time} - {history_data.get('original_filename', 'ファイル名不明')}"
                with st.expander(expander_title):
                    # 画像表示
                    gcs_uri = history_data.get('gcs_uri')
                    if gcs_uri and gcs_uri.startswith("gs://"):
                        try:
                            blob = storage.Blob.from_string(gcs_uri, client=storage_client)
                            image_bytes = blob.download_as_bytes(timeout=60)
                            st.image(image_bytes, caption=f"画像: {history_data.get('original_filename', '')}", width=300)
                        except NotFound: st.warning(f"GCS画像が見つかりません: {gcs_uri}")
                        except Exception as img_e: st.warning(f"GCS画像読み込み/表示エラー: {img_e}")
                    elif gcs_uri: st.warning(f"無効なGCS URI: {gcs_uri}")

                    # その他情報
                    st.text(f"ステータス: {history_data.get('status', 'N/A')}")
                    st.text(f"分析結果: {history_data.get('analysis_result', 'N/A')}")
                    gcs_link = history_data.get('gcs_uri', '#')
                    st.markdown(f"GCS URI: [{gcs_link}]({gcs_link.replace('gs://', 'https://storage.cloud.google.com/')})")
                    st.text(f"使用モデル: {history_data.get('gemini_model_used', 'N/A')}")
                    st.text(f"Firestore Doc ID: {doc.id}")

    except Exception as e:
        st.error(f"履歴の読み込み中にエラーが発生しました: {e}")
        st.exception(e)
    ```
    * `app.py` を保存します。

3.  **再デプロイとテスト:**
    ```bash
    # モジュール5/6と同じ gcloud run deploy コマンドを実行
    gcloud run deploy $SERVICE_NAME \
      --source . \
      --region=$REGION \
      --platform=managed \
      --allow-unauthenticated \
      --set-env-vars="BUCKET_NAME=$BUCKET_NAME,VERTEX_AI_LOCATION=$VERTEX_AI_LOCATION"
    ```
    デプロイ後、アプリにアクセスし、履歴セクションに画像付きでデータが表示されることを確認します。

---

## モジュール 8: クリーンアップ (リソースの削除)

ハンズオンで作成したリソースは課金対象となるため、不要になったら削除しましょう。

1.  **Cloud Run サービスの削除:** Google Cloud Console で [Cloud Run] -> サービス選択 -> 削除。
2.  **Cloud Storage バケットの削除:** [Cloud Storage] -> バケット選択 -> 削除。
3.  **Firestore データの削除:** [Firestore] -> データ -> コレクション選択 -> 削除。
4.  **Cloud Workstations の停止・削除:** [Cloud Workstations] -> ワークステーション選択 -> 停止/削除、及び [ワークステーション構成] -> 構成選択 -> 削除。
5.  **(Cloud Run ソースデプロイで裏で作成されたリソース):** Cloud Run がソースデプロイ時に裏で GCR や Artifact Registry にイメージを保存したり、Cloud Build を使用している場合があります。これらも不要であれば確認・削除してください ([Container Registry] / [Artifact Registry] / [Cloud Build] ページ)。

---

## まとめ と 次のステップ

お疲れ様でした！ このワークショップでは、以下の Google Cloud サービスを使って AI 画像分析アプリを構築・デプロイする流れを体験しました。

* **Cloud Workstations:** クラウドベースの開発環境
* **Streamlit:** Python での Web アプリ作成
* **Cloud Storage:** ファイルの保存
* **Cloud Run (Source Deploy):** ソースからのサーバーレスアプリ実行
* **Vertex AI (Gemini API):** AI による画像分析
* **Firestore:** 分析履歴の NoSQL データベース保存

**次のステップのアイデア:**

* Gemini プロンプトの改善
* エラーハンドリングの強化
* ユーザー認証 (IAP) の追加
* 履歴機能の強化 (検索、ページネーション)
* コスト管理の学習
* Dockerfile を使ったデプロイの検討

このハンズオンが、あなたの Google Cloud ジャーニーの一助となれば幸いです！

---

## 参考: 必要な API と IAM ロール

### 有効化が必要な API

1.  `Cloud Workstations API` (`workstations.googleapis.com`)
2.  `Compute Engine API` (`compute.googleapis.com`)
3.  `Cloud Storage API` (`storage.googleapis.com`)
4.  `Cloud Run Admin API` (`run.googleapis.com`)
5.  `Vertex AI API` (`aiplatform.googleapis.com`)
6.  `Firestore API` (`firestore.googleapis.com`)
7.  `Cloud Build API` (`cloudbuild.googleapis.com`) (Cloud Run のソースデプロイが内部で使用するため)

### 必要な主な IAM ロール

**1. ハンズオン実施ユーザー:**

* **推奨:** プロジェクト `オーナー` (`roles/owner`) または `編集者` (`roles/editor`)

**2. Cloud Run サービスアカウント (デフォルト: `[PROJECT_NUMBER]-compute@developer.gserviceaccount.com`)**

* `roles/storage.objectAdmin` (GCS 読み書き)
* `roles/aiplatform.user` (Vertex AI API 呼び出し)
* `roles/datastore.user` (Firestore 読み書き)
* **(ソースデプロイが内部で使用):** Cloud Run のソースからのデプロイ機能は、内部的に Cloud Build サービスアカウント (`[PROJECT_NUMBER]@cloudbuild.gserviceaccount.com`) を使用してコンテナイメージをビルドします。このため、Cloud Build サービスアカウントには、ソースコード (通常は一時的な GCS バケットにコピーされる) へのアクセス権や、コンテナイメージをビルドして保存 (通常は Container Registry または Artifact Registry) するための権限 (例: `roles/storage.admin`, `roles/cloudbuild.builds.builder`) が必要になります。多くの場合、これらの権限は Google Cloud によって自動的に管理・設定されますが、組織ポリシーなどで制限されている場合は、手動での権限付与が必要になる可能性があります。