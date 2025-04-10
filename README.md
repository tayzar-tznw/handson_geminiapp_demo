# ハンズオン: Google Cloud で AI 画像分析 Web アプリを作ろう！ (Gemini, Cloud Run, Firestore)

**最終更新:** 2025年4月10日

このリポジトリは、Google Cloud の各種サービスを組み合わせて AI 画像分析 Web アプリケーションを構築するハンズオンワークショップのガイドです。Cloud Workstations を開発環境として使用し、Streamlit アプリを作成、Cloud Storage への画像アップロード、Gemini API での分析、Firestore への履歴保存、そして Cloud Run へのデプロイまでをステップバイステップで学習します。

## 目次

* [対象者](#対象者)
* [学習目標](#学習目標)
* [所要時間 (目安)](#所要時間-目安)
* [必要なもの](#必要なもの)
* [モジュール 1: 開発環境のセットアップ (Cloud Workstations)](#モジュール-1-開発環境のセットアップ-cloud-workstations)
* [モジュール 2: 基本的な Web アプリの作成 (Streamlit & Git)](#モジュール-2-基本的な-web-アプリの作成-streamlit--git)
* [モジュール 3: 画像アップロード機能の追加 (Cloud Storage)](#モジュール-3-画像アップロード機能の追加-cloud-storage)
* [モジュール 4: アプリのコンテナ化と Cloud Run へのデプロイ](#モジュール-4-アプリのコンテナ化と-cloud-run-へのデプロイ)
* [モジュール 5: AI による画像分析機能の追加 (Gemini API)](#モジュール-5-ai-による画像分析機能の追加-gemini-api)
* [モジュール 6: 分析履歴の保存 (Firestore)](#モジュール-6-分析履歴の保存-firestore)
* [モジュール 7: 履歴の表示 (Firestore & GCS 画像)](#モジュール-7-履歴の表示-firestore--gcs-画像)
* [モジュール 8: クリーンアップ (リソースの削除)](#モジュール-8-クリーンアップ-リソースの削除)
* [まとめ と 次のステップ](#まとめ-と-次のステップ)

## 対象者

* Google Cloud をこれから学びたい方、初学者の方
* Python の基本的な知識がある方
* Web アプリケーション開発・デプロイに興味がある方

## 学習目標

* Cloud Workstations を使ったクラウドベースの開発環境の利用方法
* Streamlit を使った簡単な Web アプリケーションの作成
* Cloud Storage へのファイルアップロード機能の実装
* Dockerfile を用いたアプリケーションのコンテナ化
* Cloud Build と Artifact Registry を使った CI/CD パイプラインの基本
* Cloud Run へのサーバーレスアプリケーションのデプロイ
* Gemini API (Vertex AI) を使った画像分析の実装
* Firestore を使った NoSQL データベースへのデータ保存と読み取り

## 所要時間 (目安)

* 2〜3 時間

## 必要なもの

* Google Cloud プロジェクト (課金が有効になっていること)
* プロジェクト内で各種リソースを作成・管理できる権限 (オーナーまたは編集者ロール推奨)

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
    * [作成] をクリックします。
    * **名前:** `dev-config` など、わかりやすい名前を入力します。
    * **クラスタ:** 最も近いリージョンを選択します (例: `asia-northeast1` (東京))。
    * **コードエディタ:** [VS Code (Code-OSS)] またはお好みのエディタを選択します。
    * **コンテナイメージ:** デフォルトの [Base Editor (code-oss-cloudworkstations)] などで構いません。
    * 他はデフォルト設定のままで [作成] をクリックします。作成には数分かかります。

3.  **ワークステーションの起動:**
    * 作成した構成 (`dev-config`) を選択します。
    * 上部の [ワークステーション] タブに切り替え、[作成] をクリックします。
    * **名前:** `my-dev-workstation` など、ワークステーションの名前を入力します。
    * 構成で `dev-config` が選択されていることを確認し、[作成] をクリックします。起動にも数分かかります。

4.  **ワークステーションへの接続:**
    * ステータスが [実行中] になったら、ワークステーション名の横にある [起動] ボタンをクリックします。
    * ブラウザ上で VS Code (または選択したエディタ) が開きます。これがあなたの開発環境です！

---

## モジュール 2: 基本的な Web アプリの作成 (Streamlit & Git)

シンプルな Web アプリを作成し、バージョン管理を始めます。

1.  **必要なツールの確認とインストール:**
    * ワークステーションのターミナルを開きます (VS Code の場合: [Terminal] > [New Terminal])。
    * Python 仮想環境ツール `venv` が必要です。もしなければインストールします (Debian/Ubuntu ベースの場合):
        ```bash
        sudo apt update
        sudo apt install python3-venv -y
        ```

2.  **プロジェクトディレクトリの作成:**
    ```bash
    mkdir image-analysis-app
    cd image-analysis-app
    ```

3.  **Git の設定:** ソースコードを管理します。Cloud Source Repositories または GitHub/GitLab などを使用します。
    * (例: Cloud Source Repositories の場合)
        * Google Cloud Console で [Cloud Source Repositories] を開き、[リポジトリを作成] します (例: `image-analysis-app`)。
        * 表示される手順に従って Git を初期化し、リモートを追加します。
            ```bash
            git init
            # ★★★ 下の行の URL はご自身のプロジェクトに合わせて置き換えてください ★★★
            git remote add origin [https://source.developers.google.com/p/your-project-id/r/image-analysis-app](https://source.developers.google.com/p/your-project-id/r/image-analysis-app)
            ```
    * (GitHub 等の場合も同様に `git init` と `git remote add origin <your-repo-url>` を実行)

4.  **Python 仮想環境の作成と有効化:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # プロンプトの先頭に (venv) と表示されればOK
    ```

5.  **Streamlit のインストール:**
    ```bash
    pip install streamlit
    ```

6.  **"Hello World" アプリの作成 (`app.py`):**
    ```python
    # app.py
    import streamlit as st

    st.title("画像分析アプリ (v0.1)")
    st.header("Hello, Google Cloud!")
    st.write("Cloud Workstations で開発中！")
    ```

7.  **動作確認:**
    ```bash
    streamlit run app.py
    ```
    ターミナルに URL が表示されます。[Open in Browser] ボタンが表示されたらクリックするか、表示されたポート (通常 8501) を手動で転送設定して `localhost:8501` にアクセスします。"Hello, Google Cloud!" が表示されたら、ターミナルで `Ctrl+C` を押してアプリを停止します。

8.  **`requirements.txt` の作成:** アプリの依存ライブラリを記録します。
    ```bash
    pip freeze > requirements.txt
    ```

9.  **`.gitignore` ファイルの作成:** Git で管理しないファイルを指定します。
    ```text
    # .gitignore
    venv/
    __pycache__/
    *.pyc
    .streamlit/
    ```

10. **Git への Commit と Push:**
    ```bash
    git add .
    git commit -m "Initial commit: Basic Streamlit app"
    git push -u origin main # または master
    ```

---

## モジュール 3: 画像アップロード機能の追加 (Cloud Storage)

ユーザーが画像をアップロードし、それをクラウドに保存する機能を追加します。

1.  **API の有効化:**
    * Google Cloud Console で `Cloud Storage API` を検索し、有効にします。

2.  **GCS バケットの作成:** 画像を保存する場所を作成します。
    * ナビゲーションメニューから [Cloud Storage] > [バケット] を選択します。
    * [作成] をクリックします。
    * **名前:** **世界中で一意 (ユニーク)** な名前を入力します (例: `your-project-id-image-bucket`)。 **`your-project-id-image-bucket` を実際に使うバケット名に置き換えてください。**
    * **ロケーションタイプ:** `Region` を選択し、ワークステーションやアプリ実行場所に近いリージョン (例: `asia-northeast1`) を選択します。
    * **ストレージクラス:** `Standard` のままでOKです。
    * **アクセス制御:** `均一` (Uniform) を選択します。
    * **公開アクセスの防止:** 「このバケットで公開アクセス禁止を適用します」にチェックが入っていることを確認します (非公開が基本)。
    * [作成] をクリックします。

3.  **必要なライブラリのインストール:**
    ```bash
    # (venv が有効な状態で)
    pip install google-cloud-storage
    ```

4.  **`requirements.txt` の更新:**
    ```bash
    pip freeze > requirements.txt
    ```

5.  **`app.py` の修正:**
    ```python
    # app.py の修正・追記
    import streamlit as st
    from google.cloud import storage
    import os
    import uuid # 一意なファイル名生成のため

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
        # st.stop() # 必要なら停止

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
    **【重要】** コード中の `your-project-id` と `your-project-id-image-bucket` を、ご自身のプロジェクト ID と作成した GCS バケット名に**必ず置き換えてください**。

6.  **認証と権限:**
    * Cloud Workstations でこのコードを実行する場合、GCS への書き込み権限が必要です。ターミナルで以下のコマンドを実行して、自身のユーザーアカウントで認証します (Application Default Credentials: ADC)。
        ```bash
        gcloud auth application-default login
        ```
        ブラウザが開き、ログインを求められます。承認すると、SDK はこの認証情報を使って GCS にアクセスします。
    * ご自身のユーザーアカウントには、対象バケットへの書き込み権限が必要です。プロジェクトの「編集者」ロールや、より限定的な `roles/storage.objectAdmin` / `roles/storage.objectCreator` を Google Cloud Console の IAM ページで確認・付与してください。

7.  **動作確認:**
    * `app.py` を保存し、ターミナルで `streamlit run app.py` を実行します。
    * ブラウザでアプリを開き、画像ファイルを選択して [画像を GCS にアップロード] ボタンをクリックします。
    * 成功メッセージが表示され、Google Cloud Console の Cloud Storage ブラウザでバケット内にファイルがアップロードされていることを確認します。

8.  **Git への Commit と Push:**
    ```bash
    git add app.py requirements.txt
    git commit -m "Feat: Add image upload to GCS"
    git push
    ```

---

## モジュール 4: アプリのコンテナ化と Cloud Run へのデプロイ

作成したアプリをコンテナに入れ、サーバーレス環境 Cloud Run で動かせるようにします。Cloud Build でビルドとデプロイを自動化します。

1.  **API の有効化:**
    * 以下の API を Google Cloud Console で検索し、有効にします:
        * `Cloud Build API`
        * `Artifact Registry API`
        * `Cloud Run Admin API`

2.  **Artifact Registry Docker リポジトリの作成:** ビルドしたコンテナイメージを保存する場所です。
    ```bash
    # ★★★ image-analysis-repo を任意のリポジトリ名に置き換え可能 ★★★
    # ★★★ asia-northeast1 を使用するリージョンに置き換え ★★★
    gcloud artifacts repositories create image-analysis-repo \
        --repository-format=docker \
        --location=asia-northeast1 \
        --description="Docker repository for Image Analysis App"
    ```

3.  **`Dockerfile` の作成:** コンテナイメージの設計図です。プロジェクトのルート (`app.py` と同じ場所) に作成します。
    ```dockerfile
    # Dockerfile

    # ベースイメージを選択 (Python 3.11 のスリム版)
    FROM python:3.11-slim

    # 環境変数: Cloud Run がリッスンするポートとPythonログ設定
    ENV PORT 8080
    ENV PYTHONUNBUFFERED TRUE

    # 作業ディレクトリ
    WORKDIR /app

    # 依存関係をインストール
    COPY requirements.txt ./
    # --no-cache-dir でキャッシュを使わずディスク容量節約
    RUN pip install --no-cache-dir -r requirements.txt

    # アプリケーションコードをコピー
    COPY . .

    # コンテナがリッスンするポートを公開 (ドキュメンテーション目的)
    EXPOSE ${PORT}

    # コンテナ起動時に実行されるコマンド
    # シェル経由で実行し、${PORT} 環境変数を展開させる
    CMD sh -c "streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0 --server.enableCORS=false"
    ```

4.  **`cloudbuild.yaml` の作成:** Cloud Build にビルドとデプロイの手順を指示します。プロジェクトのルートに作成します。
    ```yaml
    # cloudbuild.yaml
    steps:
    # 1. Docker イメージをビルド
    - name: 'gcr.io/cloud-builders/docker'
      args: [
          'build',
          '-t',
          # ★★★ 下の行のリージョン、リポジトリ名、イメージ名を環境に合わせて変更 ★★★
          'asia-northeast1-docker.pkg.dev/$PROJECT_ID/image-analysis-repo/image-analysis-app:latest',
          '.'
      ]
      id: 'Build Image'

    # 2. イメージを Artifact Registry にプッシュ
    - name: 'gcr.io/cloud-builders/docker'
      args: ['push', 'asia-northeast1-docker.pkg.dev/$PROJECT_ID/image-analysis-repo/image-analysis-app:latest']
      id: 'Push Image'
      waitFor: ['Build Image']

    # 3. Cloud Run にデプロイ
    - name: 'google/cloud-sdk:latest'
      entrypoint: gcloud
      args: [
          'run', 'deploy', 'image-analysis-service', # ★★★ Cloud Run サービス名 (任意) ★★★
          '--image=asia-northeast1-docker.pkg.dev/$PROJECT_ID/image-analysis-repo/image-analysis-app:latest',
          '--region=asia-northeast1', # ★★★ リージョンを環境に合わせる ★★★
          '--platform=managed',
          # '--service-account=your-service-account@your-project-id.iam.gserviceaccount.com', # (推奨) 専用SAを使う場合
          # ★★★ 次の行はテスト用に認証なしアクセスを許可。本番では非推奨 ★★★
          '--allow-unauthenticated',
          # ★★★ 環境変数を設定 (BUCKET_NAMEは実際のバケット名に) ★★★
          '--set-env-vars=GOOGLE_CLOUD_PROJECT=$PROJECT_ID,BUCKET_NAME=your-project-id-image-bucket'
      ]
      id: 'Deploy to Cloud Run'
      waitFor: ['Push Image']

    images:
    - 'asia-northeast1-docker.pkg.dev/$PROJECT_ID/image-analysis-repo/image-analysis-app:latest'

    timeout: '1200s'
    ```
    **【重要】**
    * ファイル内の `★★★` が付いている箇所 (リージョン、リポジトリ名、Cloud Run サービス名、バケット名) をご自身の環境に合わせて**必ず修正・確認**してください。
    * `--allow-unauthenticated`: 誰でもアクセスできるサービスになります。**学習目的以外では非推奨**です。組織ポリシーによってはエラーになる場合があります。
    * `--set-env-vars`: ここで Cloud Run 上のアプリケーションで使う環境変数を設定します。`BUCKET_NAME` の値 (`your-project-id-image-bucket`) は実際のバケット名に置き換えてください。

5.  **`app.py` の環境変数対応:** `app.py` の設定部分を修正し、ハードコードされた値を環境変数から読み込むようにします。
    ```python
    # app.py の設定部分を修正
    import os # ファイル先頭で import

    # --- 設定 ---
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    BUCKET_NAME = os.getenv("BUCKET_NAME")

    # 環境変数が設定されていない場合のエラー処理 (推奨)
    if not PROJECT_ID:
        st.error("環境変数 GOOGLE_CLOUD_PROJECT が設定されていません。")
        st.stop() # アプリを停止
    if not BUCKET_NAME:
        st.error("環境変数 BUCKET_NAME が設定されていません。")
        st.stop() # アプリを停止

    # --- GCS クライアントの初期化 ---
    # ... (変更なし) ...
    ```

6.  **Git への Commit と Push:**
    ```bash
    git add Dockerfile cloudbuild.yaml app.py
    git commit -m "Feat: Add Dockerfile, cloudbuild.yaml, env var support"
    git push
    ```

7.  **Cloud Build サービスアカウントへの権限付与:** Cloud Build がイメージをプッシュし、Cloud Run にデプロイするために権限が必要です。
    * プロジェクト番号を取得:
        ```bash
        # ★★★ $PROJECT_ID を実際のプロジェクトIDに置き換えるか、環境変数として設定 ★★★
        export PROJECT_ID="your-project-id"
        PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
        ```
    * Cloud Build サービスアカウント (`[PROJECT_NUMBER]@cloudbuild.gserviceaccount.com`) に以下のロールを付与します:
        ```bash
        # Artifact Registry 書き込み権限
        gcloud projects add-iam-policy-binding $PROJECT_ID \
            --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
            --role="roles/artifactregistry.writer"

        # Cloud Run 管理者権限
        gcloud projects add-iam-policy-binding $PROJECT_ID \
            --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
            --role="roles/run.admin"

        # Cloud Run サービスアカウントとして動作する権限 (重要)
        gcloud projects add-iam-policy-binding $PROJECT_ID \
            --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
            --role="roles/iam.serviceAccountUser" \
            --condition=None # 確認プロンプトが出る場合あり
        ```

8.  **Cloud Run サービスアカウントへの権限付与:** Cloud Run 上で動作するアプリが GCS にアクセスするために権限が必要です。
    * **サービスアカウントの特定:** デフォルトでは **Compute Engine のデフォルトサービスアカウント** (`[PROJECT_NUMBER]-compute@developer.gserviceaccount.com`) が使われます。
    * **権限の付与:** このサービスアカウントに GCS バケットへのアクセス権限を付与します。
        ```bash
        # ★★★ $BUCKET_NAME を実際のバケット名に置き換えるか、環境変数として設定 ★★★
        export BUCKET_NAME="your-project-id-image-bucket"
        gcloud storage buckets add-iam-policy-binding gs://$BUCKET_NAME \
            --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
            --role="roles/storage.objectAdmin"
        ```

9.  **Cloud Build の実行:**
    * ワークステーションのターミナルで、プロジェクトのルートディレクトリ (`cloudbuild.yaml` がある場所) にいることを確認します。
    * 以下のコマンドでビルドとデプロイを実行します:
        ```bash
        gcloud builds submit --config cloudbuild.yaml .
        ```
    * ビルドとデプロイには数分かかります。最後に Cloud Run サービスの URL が表示されれば成功です。

10. **デプロイの確認:**
    * Cloud Build の出力や、Google Cloud Console の [Cloud Run] ページでサービスの URL を確認します。
    * URL にブラウザでアクセスし、Streamlit アプリが表示されることを確認します。
    * 画像をアップロードし、GCS に保存されることを確認します。

---

## モジュール 5: AI による画像分析機能の追加 (Gemini API)

アップロードされた画像を Gemini API に渡し、画像の内容を分析させます。

1.  **API の有効化:**
    * Google Cloud Console で `Vertex AI API` を検索し、有効にします。

2.  **必要なライブラリのインストール:** (Firestore も先に入れておきます)
    ```bash
    # (venv が有効な状態で)
    pip install google-cloud-aiplatform google-cloud-firestore pytz # pytz はタイムゾーン用(任意)
    ```

3.  **`requirements.txt` の更新:**
    ```bash
    pip freeze > requirements.txt
    ```

4.  **IAM 権限の付与:** Cloud Run サービスアカウント (例: Compute Engine default SA) に Vertex AI API を呼び出す権限を付与します。
    ```bash
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role="roles/aiplatform.user"
    ```

5.  **環境変数の準備:**
    * Vertex AI を初期化するためにリージョン情報が必要です。`cloudbuild.yaml` やローカル実行時に `VERTEX_AI_LOCATION` 環境変数を設定します (例: `us-central1`, `asia-northeast1` など、Gemini モデルが利用可能なリージョン)。

6.  **`app.py` の修正:** Gemini API 呼び出しと Firestore クライアント初期化を追加します。
    ```python
    # app.py の修正・追記

    # --- import 文の追加 ---
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
    # タイムゾーン用 (オプション)
    try: from zoneinfo import ZoneInfo
    except ImportError:
        try: import pytz; ZoneInfo = pytz.timezone
        except ImportError: ZoneInfo = None

    # --- 設定 (環境変数読み込み) ---
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    VERTEX_AI_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1") # デフォルト設定

    # 環境変数チェック
    if not PROJECT_ID or not BUCKET_NAME or not VERTEX_AI_LOCATION:
        st.error("環境変数 (GOOGLE_CLOUD_PROJECT, BUCKET_NAME, VERTEX_AI_LOCATION) が不足しています。")
        st.stop()

    # --- Vertex AI / Firestore クライアントの初期化 ---
    try:
        vertexai.init(project=PROJECT_ID, location=VERTEX_AI_LOCATION)
        model = GenerativeModel("gemini-1.5-flash-001")
        db = firestore.Client(project=PROJECT_ID)
    except Exception as e:
        st.error(f"Vertex AI / Firestore クライアント初期化失敗: {e}")
        st.stop()

    # --- GCS クライアントの初期化 ---
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
    except Exception as e:
        st.error(f"GCS クライアント初期化失敗: {e}")
        st.stop()

    # --- Streamlit アプリケーション ---
    st.title("画像分析アプリ (v1.0)")
    st.write(f"Project: {PROJECT_ID}, Bucket: {BUCKET_NAME}, Vertex AI Location: {VERTEX_AI_LOCATION}") # 設定値確認用(任意)

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
                        [image_part, prompt],
                        generation_config=generation_config,
                        stream=False
                    )

                    if response.candidates and response.candidates[0].content.parts:
                        gemini_result_text = response.text.strip()
                        analysis_result = gemini_result_text
                        status = "Success"
                        st.write("Gemini 解析完了")
                    else:
                        # エラー詳細の取得試行
                        gemini_result_text = "Gemini 解析失敗 (空またはブロックされた応答)"
                        try:
                             block_reason = response.candidates[0].finish_reason
                             safety_ratings = response.candidates[0].safety_ratings
                             gemini_result_text += f" (理由: {block_reason}, Safety: {safety_ratings})"
                        except Exception: pass
                        status = "Gemini API Error"
                        st.warning(gemini_result_text)

                    st.subheader("Gemini 分析結果:")
                    st.markdown(f"```\n{analysis_result}\n```")

                    # 3. Firestore Write
                    st.write("3/3: 解析履歴を Firestore に保存中...")
                    doc_ref = db.collection("image_analysis_history").document() # ★★★ コレクション名 ★★★
                    data_to_save = {
                        "timestamp": upload_timestamp,
                        "gcs_uri": gcs_uri,
                        "original_filename": uploaded_file.name,
                        "content_type": mime_type,
                        "gemini_model_used": model.name,
                        "gemini_result_text": gemini_result_text,
                        "analysis_result": analysis_result,
                        "status": status,
                    }
                    doc_ref.set(data_to_save)
                    st.success(f"Firestore に履歴を保存しました (Doc ID: {doc_ref.id})")

                except Exception as e:
                    status = "Processing Error"
                    error_message = f"処理中にエラー: {str(e)}"
                    st.error(error_message)
                    st.exception(e)
                    # エラー時の記録 (オプション)
                    if gcs_uri: # Uploadは成功した場合のみ
                         try:
                            doc_ref = db.collection("image_analysis_history").document()
                            data_to_save = {
                                "timestamp": upload_timestamp, "gcs_uri": gcs_uri, "original_filename": uploaded_file.name,
                                "content_type": uploaded_file.type, "status": status, "gemini_result_text": error_message,
                                "analysis_result": "Error"
                            }
                            doc_ref.set(data_to_save)
                            st.info("エラー情報をFirestoreに記録しました。")
                         except Exception as db_e:
                            st.error(f"エラー情報のFirestore保存に失敗: {db_e}")

    # --- 解析履歴表示セクション (次のモジュールで実装) ---
    st.divider()
    st.subheader("解析履歴 (直近10件)")
    # ... (ここに履歴表示コードが入る) ...
    ```

7.  **`cloudbuild.yaml` の更新:** `VERTEX_AI_LOCATION` 環境変数を追加します。
    ```yaml
    # cloudbuild.yaml の gcloud run deploy ステップを修正
    # ...
          # ★★★ VERTEX_AI_LOCATION を追加 (リージョンは適宜変更) ★★★
          '--set-env-vars=GOOGLE_CLOUD_PROJECT=$PROJECT_ID,BUCKET_NAME=your-project-id-image-bucket,VERTEX_AI_LOCATION=us-central1',
    # ...
    ```

8.  **Git への Commit と Push:**
    ```bash
    git add app.py requirements.txt cloudbuild.yaml
    git commit -m "Feat: Integrate Gemini API for image analysis"
    git push
    ```

9.  **再デプロイとテスト:**
    ```bash
    gcloud builds submit --config cloudbuild.yaml .
    ```
    デプロイ後、Cloud Run の URL にアクセスし、画像分析を実行します。Gemini の結果が表示されれば成功です。エラー `Project ... is not allowed to use Publisher Model ...` が発生した場合は、モデル名の指定、環境変数 (`PROJECT_ID`, `VERTEX_AI_LOCATION`)、SDK バージョン、API 有効化、IAM 権限を確認してください。

---

## モジュール 6: 分析履歴の保存 (Firestore)

Gemini の分析結果を含む処理履歴を Firestore データベースに保存します。

* **このステップの実装は、モジュール 5 の `app.py` 修正内容に含まれています。**

1.  **API の有効化:**
    * Google Cloud Console で `Firestore API` を検索し、有効にします。
    * 初めて Firestore を使う場合、[Firestore] ページに移動し、[データベースの作成] をクリックします。
        * **モード:** **Native モード** を選択します。
        * **ロケーション:** アプリや GCS に近いリージョン (例: `asia-northeast1`) を選択します。
        * **【注意】モードとロケーションは後から変更できません。**

2.  **必要なライブラリのインストール:** (モジュール 5 で実施済み)

3.  **`requirements.txt` の更新:** (モジュール 5 で実施済み)

4.  **IAM 権限の付与:** Cloud Run サービスアカウントに Firestore への書き込み権限を付与します。
    ```bash
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role="roles/datastore.user"
    ```

5.  **`app.py` の修正:** (モジュール 5 で実施済み)
    * Firestore クライアント初期化、コレクション参照、データ書き込みが実装されています。コレクション名は `image_analysis_history` としています。

6.  **再デプロイとテスト:**
    * (コード変更があれば `git commit`, `git push`)
    * `gcloud builds submit --config cloudbuild.yaml .` で再デプロイします。
    * 画像分析を実行し、成功メッセージを確認します。
    * Google Cloud Console の [Firestore] ページで `image_analysis_history` コレクションを開き、データが保存されていることを確認します。

---

## モジュール 7: 履歴の表示 (Firestore & GCS 画像)

Firestore に保存した履歴と、対応する画像をアプリ内に表示します。

1.  **(オプション) `pytz` のインストール:** (モジュール 5 で実施済み or 不要ならスキップ)

2.  **`app.py` の修正:** ファイル末尾の履歴表示セクションを実装します。

    ```python
    # app.py の修正 (ファイル末尾に追加)

    # ... (これまでのコード) ...

    # --- 解析履歴表示セクション ---
    st.divider()
    st.subheader("解析履歴 (直近10件)")

    # タイムゾーン処理の準備
    jst = None
    try: from zoneinfo import ZoneInfo; jst = ZoneInfo('Asia/Tokyo')
    except ImportError:
        try: import pytz; jst = pytz.timezone('Asia/Tokyo')
        except ImportError: pass # タイムゾーン処理不可

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

                # タイムスタンプ表示処理
                timestamp_utc = history_data.get('timestamp')
                display_time = "時刻不明"
                if timestamp_utc:
                    if jst:
                         try: display_time = timestamp_utc.astimezone(jst).strftime('%Y-%m-%d %H:%M:%S %Z')
                         except: display_time = "TZ変換エラー" # エラー処理を簡略化
                    else:
                         try: display_time = timestamp_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
                         except: display_time = "時刻フォーマットエラー"

                # Expander で表示
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

3.  **IAM 権限の確認:** Cloud Run サービスアカウントに GCS バケットからの読み取り権限 (`roles/storage.objectViewer`) が必要です。

4.  **Git への Commit と Push:**
    ```bash
    git add app.py requirements.txt # pytz を追加した場合など
    git commit -m "Feat: Display history with images from Firestore"
    git push
    ```

5.  **再デプロイとテスト:**
    ```bash
    gcloud builds submit --config cloudbuild.yaml .
    ```
    デプロイ後、アプリにアクセスし、履歴セクションに画像付きでデータが表示されることを確認します。

---

## モジュール 8: クリーンアップ (リソースの削除)

ハンズオンで作成したリソースは課金対象となるため、不要になったら削除しましょう。

1.  **Cloud Run サービスの削除:** Google Cloud Console で [Cloud Run] -> サービス選択 -> 削除。
2.  **Artifact Registry リポジトリの削除:** [Artifact Registry] -> リポジトリ選択 -> 削除。
3.  **Cloud Storage バケットの削除:** [Cloud Storage] -> バケット選択 -> 削除。
4.  **Firestore データの削除:** [Firestore] -> データ -> コレクション選択 -> 削除。
5.  **Cloud Workstations の停止・削除:** [Cloud Workstations] -> ワークステーション選択 -> 停止/削除、及び [ワークステーション構成] -> 構成選択 -> 削除。
6.  **Cloud Build 履歴 (任意):** [Cloud Build] -> 履歴 -> 削除。

---

## まとめ と 次のステップ

お疲れ様でした！ これで、Google Cloud の主要サービスを連携させ、AI 画像分析 Web アプリを構築・デプロイする基本的な流れを体験できました。

**次のステップのアイデア:**

* Gemini プロンプトの工夫
* エラーハンドリングの強化
* ユーザー認証 (IAP) の追加
* CI/CD トリガーの設定
* 履歴機能の強化 (検索、ページネーション)
* コスト管理の学習

このハンズオンが、あなたの Google Cloud ジャーニーの一助となれば幸いです！