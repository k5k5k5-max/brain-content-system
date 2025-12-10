# Googleドライブ連携セットアップガイド

このガイドでは、Brain Content Systemで生成した記事を自動的にGoogleドライブにアップロードするための設定方法を説明します。

---

## 🎯 必要なもの

1. **Googleアカウント**
2. **Google Cloud Platform（GCP）プロジェクト**
3. **サービスアカウント**（Google Drive API用）

---

## 📋 セットアップ手順

### ステップ1: Google Cloud Platformでプロジェクトを作成

1. **Google Cloud Consoleにアクセス**  
   👉 https://console.cloud.google.com/

2. **新しいプロジェクトを作成**
   - 左上の「プロジェクトを選択」をクリック
   - 「新しいプロジェクト」をクリック
   - プロジェクト名: `brain-content-system`
   - 「作成」をクリック

---

### ステップ2: Google Drive APIを有効化

1. **APIライブラリに移動**  
   👉 https://console.cloud.google.com/apis/library

2. **「Google Drive API」を検索**
   - 検索ボックスに「Google Drive API」と入力
   - 結果から「Google Drive API」をクリック
   - 「有効にする」をクリック

---

### ステップ3: サービスアカウントを作成

1. **IAMと管理 → サービスアカウントに移動**  
   👉 https://console.cloud.google.com/iam-admin/serviceaccounts

2. **「サービスアカウントを作成」をクリック**

3. **サービスアカウントの詳細を入力**
   - サービスアカウント名: `brain-drive-uploader`
   - サービスアカウントID: `brain-drive-uploader`（自動生成）
   - 説明: `Brain記事をGoogleドライブにアップロード`
   - 「作成して続行」をクリック

4. **権限の付与（スキップ）**
   - 「続行」をクリック

5. **完了**
   - 「完了」をクリック

---

### ステップ4: JSONキーを作成してダウンロード

1. **作成したサービスアカウントをクリック**
   - 一覧から `brain-drive-uploader@...` をクリック

2. **「キー」タブに移動**
   - 上部の「キー」タブをクリック

3. **「鍵を追加」→「新しい鍵を作成」をクリック**
   - キーのタイプ: `JSON`を選択
   - 「作成」をクリック

4. **JSONファイルがダウンロードされます**
   - ファイル名（例）: `brain-content-system-abc123def456.json`
   - **このファイルは安全に保管してください！**

---

### ステップ5: サービスアカウントにGoogleドライブへのアクセス権を付与

1. **Googleドライブを開く**  
   👉 https://drive.google.com/

2. **共有フォルダを開く**
   - あなたが作成したフォルダ: https://drive.google.com/drive/folders/1P8RssQ4VfMCmc-cB6NelrAtMKVljNdg_

3. **フォルダを右クリック → 「共有」をクリック**

4. **サービスアカウントのメールアドレスを追加**
   - ステップ4でダウンロードしたJSONファイルを開く
   - `client_email` の値をコピー（例: `brain-drive-uploader@brain-content-system.iam.gserviceaccount.com`）
   - Googleドライブの共有画面にペースト
   - 権限: **編集者**
   - 「送信」をクリック

---

### ステップ6: ローカル環境でのセットアップ

#### 方法A: 環境変数で設定（推奨）

```bash
# JSONファイルを安全な場所に配置
mkdir -p ~/.config/gcloud
mv ~/Downloads/brain-content-system-abc123def456.json ~/.config/gcloud/brain-drive-service-account.json

# 環境変数を設定
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/brain-drive-service-account.json"

# .zshrc または .bashrc に追加（永続化）
echo 'export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/brain-drive-service-account.json"' >> ~/.zshrc
source ~/.zshrc
```

#### 方法B: プロジェクトルートに配置

```bash
# JSONファイルをプロジェクトルートに配置
cd /Users/keigo/001_cursor/Brain_Content_System_Ver2
cp ~/Downloads/brain-content-system-abc123def456.json ./brain-drive-credentials.json

# .gitignore に追加（重要！）
echo "brain-drive-credentials.json" >> .gitignore
```

---

### ステップ7: GitHub Actionsでのセットアップ

1. **GitHubリポジトリのSecretsに追加**
   - GitHubリポジトリを開く
   - 「Settings」→「Secrets and variables」→「Actions」
   - 「New repository secret」をクリック

2. **Secretを追加**
   - Name: `GOOGLE_DRIVE_CREDENTIALS`
   - Value: JSONファイルの**全内容**をコピペ
     ```json
     {
       "type": "service_account",
       "project_id": "brain-content-system",
       "private_key_id": "...",
       "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
       "client_email": "brain-drive-uploader@brain-content-system.iam.gserviceaccount.com",
       ...
     }
     ```
   - 「Add secret」をクリック

---

## ✅ 動作確認

### ローカルでテスト

```bash
cd /Users/keigo/001_cursor/Brain_Content_System_Ver2/00_System

# 1記事生成してGoogleドライブにアップロード
python3 master_generator.py \
  --theme "テスト記事" \
  --target "テストユーザー" \
  --config test_config.json
```

成功すると、以下のように表示されます：

```
📤 Phase 6: Googleドライブアップロード
  ├─ 認証中... (/Users/keigo/.config/gcloud/brain-drive-service-account.json)
  │  └─ ✅ 認証成功
  ├─ 年月フォルダを確認中... (2024年12月)
  │  └─ ✅ フォルダID: abc123
  ├─ テーマフォルダを作成中... (20241210_テスト記事)
  │  └─ ✅ フォルダID: def456
  ├─ final_article.md アップロード中...
  │  └─ ✅ 完了
  ├─ final_article.html アップロード中...
  │  └─ ✅ 完了
  ├─ 画像フォルダをアップロード中...
  │  └─ ✅ 23枚の画像をアップロード完了
  └─ ✅ アップロード完了

📂 Googleドライブ: https://drive.google.com/drive/folders/def456
```

### GitHub Actionsでテスト

1. **GitHub Actionsを手動実行**
   👉 https://github.com/k5k5k5-max/brain-content-system/actions

2. **「Brain Daily Batch」を選択**
   - 「Run workflow」をクリック
   - 「Run workflow」（緑ボタン）をクリック

3. **LINEに通知が届くか確認**
   - ✅ バッチ開始通知
   - ✅ 各記事の完了通知（ドライブURL付き）
   - ✅ バッチ完了サマリー

---

## 🔧 トラブルシューティング

### エラー: `認証情報が見つかりません`

**原因**: 環境変数が設定されていない

**解決策**:
```bash
# 環境変数を確認
echo $GOOGLE_APPLICATION_CREDENTIALS

# 設定されていない場合
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/brain-drive-service-account.json"
```

---

### エラー: `403 Forbidden`

**原因**: サービスアカウントにフォルダへのアクセス権がない

**解決策**:
1. Googleドライブで共有フォルダを開く
2. フォルダを右クリック → 「共有」
3. サービスアカウントのメールアドレスを追加（編集者権限）

---

### エラー: `The caller does not have permission`

**原因**: Google Drive APIが有効化されていない

**解決策**:
1. Google Cloud Consoleでプロジェクトを選択
2. APIライブラリ → Google Drive APIを検索
3. 「有効にする」をクリック

---

## 📁 アップロード先のフォルダ構造

```
Brain記事/
├── 2024年12月/
│   ├── 20241210_Threadsで月5万円稼ぐ方法/
│   │   ├── final_article.md
│   │   ├── final_article.html
│   │   └── images/
│   │       ├── banner_01.png
│   │       ├── ill_01.png
│   │       └── ...
│   ├── 20241210_ChatGPTで副業を始める方法/
│   │   └── ...
│   └── 20241211_Instagramで稼ぐ方法/
│       └── ...
└── 2025年01月/
    └── ...
```

---

## 🎉 完了！

これで、Brain Content Systemで生成した記事が自動的にGoogleドライブにアップロードされるようになりました。

外注さんには、共有フォルダのリンクを送るだけで、記事をダウンロードしてBrain/Tipsにアップロードしてもらえます。

