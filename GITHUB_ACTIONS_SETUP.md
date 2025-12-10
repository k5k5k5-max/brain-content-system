# GitHub Actions自動実行セットアップガイド

このガイドに従って、Brain記事生成システムをGitHub Actionsで自動実行（毎日定期実行）できるようにします。

---

## 📋 前提条件

- GitHubアカウント
- Gemini APIキー（テキスト生成用）
- LINE Notify トークン（通知用）

---

## 🚀 セットアップ手順

### ステップ1: GitHubにコードをpush（5分）

ターミナルで以下を実行：

```bash
cd /Users/keigo/001_cursor/Brain_Content_System_Ver2

# Gitリポジトリ初期化
git init

# 全ファイルをステージング
git add .

# コミット
git commit -m "Initial commit: Brain content generation system"

# メインブランチ名を設定
git branch -M main

# リモートリポジトリを追加
git remote add origin https://github.com/k5k5k5-max/brain-content-system.git

# GitHubにpush
git push -u origin main
```

### ステップ2: GitHub Secretsを設定（3分）

#### 2-1. Secrets設定画面を開く

👉 https://github.com/k5k5k5-max/brain-content-system/settings/secrets/actions

#### 2-2. APIキーを登録

「**New repository secret**」ボタンをクリックして、以下を1つずつ登録：

| Name | Value | 取得方法 |
|------|-------|----------|
| **GEMINI_API_KEY** | あなたのGemini APIキー | `/Users/keigo/001_cursor/.env` ファイルの中の `GEMINI_API_KEY=` の値 |
| **LINE_NOTIFY_TOKEN** | あなたのLINE Notifyトークン | `/Users/keigo/001_cursor/.env` ファイルの中の `LINE_NOTIFY_TOKEN=` の値 |

**登録手順（各Secret）:**
1. 「New repository secret」をクリック
2. Name: 上記の表の「Name」を入力
3. Value: 対応する値を貼り付け
4. 「Add secret」をクリック

**オプション（Claudeを使う場合のみ）:**

| Name | Value |
|------|-------|
| **ANTHROPIC_API_KEY** | あなたのClaude APIキー |

**注意:** Geminiだけで動くので、Claudeは不要です。

---

### ステップ3: テーマリストを編集（2分）

生成したい記事のテーマを設定します。

#### 3-1. ファイルを編集

```bash
cd /Users/keigo/001_cursor/Brain_Content_System_Ver2
nano 00_System/theme_list.txt
```

#### 3-2. テーマを追加（1行1テーマ）

例: 毎日10本生成したい場合は10行書く

```
Threadsで月5万円稼ぐ方法
ChatGPTで副業を始める完全ガイド
Instagram攻略法2025年版
TikTokでバズる動画の作り方
Notion活用術で生産性3倍
Canvaデザイン完全マスター
副業で月10万稼ぐロードマップ
AI時代の働き方改革
ストック型ビジネスの始め方
コンテンツ販売で稼ぐ方法
```

#### 3-3. 保存してpush

```bash
# 保存（nanoの場合: Ctrl+O → Enter → Ctrl+X）

# GitHubにpush
git add 00_System/theme_list.txt
git commit -m "Update theme list"
git push
```

---

### ステップ4: 手動実行でテスト（2分）

#### 4-1. Actions画面を開く

👉 https://github.com/k5k5k5-max/brain-content-system/actions

#### 4-2. ワークフローを有効化（初回のみ）

緑色のボタン「**I understand my workflows, go ahead and enable them**」をクリック

#### 4-3. 手動実行

1. 左側のメニューから「**Brain Daily Batch**」を選択
2. 右側の「**Run workflow**」ボタンをクリック
3. 「**Run workflow**」（緑ボタン）を再度クリック

#### 4-4. 実行状況を確認

- 🟡 黄色の●：実行中
- ✅ 緑のチェック：成功
- ❌ 赤のX：失敗（クリックしてログを確認）

#### 4-5. LINE通知を確認

成功すると、LINEに以下の通知が届きます：
- 「🚀 Brain記事生成バッチ開始」
- 各テーマの処理状況
- 「✅ Brain記事生成バッチ完了」

---

### ステップ5: 定期実行の確認

テストが成功すれば、**あとは自動**です！

- **毎日 JST 12:30（UTC 03:30）** に自動実行
- Macがスリープでも、電源OFFでも動きます
- GitHub Actionsのクラウドで実行されます

**実行時刻を変更したい場合:**

`.github/workflows/brain_batch.yml` の以下の行を編集：

```yaml
schedule:
  - cron: '30 3 * * *'  # UTC時刻（JSTは+9時間）
```

例）
- JST 朝7時 → `cron: '0 22 * * *'`（前日22:00 UTC）
- JST 昼12時 → `cron: '0 3 * * *'`（03:00 UTC）
- JST 夜21時 → `cron: '0 12 * * *'`（12:00 UTC）

---

## 📊 生成された記事の確認

### Actions画面でログを確認

👉 https://github.com/k5k5k5-max/brain-content-system/actions

各実行をクリック → 「batch-runner」→ ログ展開で進捗確認

### 生成ファイルをダウンロード

1. Actions実行画面の下部「Artifacts」セクション
2. 「batch-logs」をクリックしてダウンロード
3. ZIPを解凍して `/tmp/brain_batch_logs/<batch_id>/` 内のログを確認

**注意:** 生成された記事本体（Markdown/HTML/画像）は現在Artifactに含まれていません。必要な場合は、別途S3やGoogleDrive等にアップロードする処理を追加できます。

---

## 🔧 トラブルシューティング

### Q: 「Secrets not found」エラーが出る

**A:** Secretsが正しく設定されているか確認
- https://github.com/k5k5k5-max/brain-content-system/settings/secrets/actions
- `GEMINI_API_KEY` と `LINE_NOTIFY_TOKEN` が登録されているか確認

### Q: 「ModuleNotFoundError」が出る

**A:** `requirements.txt` が不足している可能性があります。以下を実行：

```bash
cd /Users/keigo/001_cursor/Brain_Content_System_Ver2
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

### Q: LINE通知が来ない

**A:** 以下を確認
1. `LINE_NOTIFY_TOKEN` が正しくSecretsに登録されているか
2. LINEアプリで「LINE Notify」とのトークルームが作成されているか
3. トークンが有効期限切れになっていないか

### Q: Geminiでエラーが出る

**A:** 以下を確認
1. `GEMINI_API_KEY` が正しいか
2. Gemini APIの無料枠を超えていないか
3. APIキーがアクティブになっているか

### Q: テーマが処理されない

**A:** 以下を確認
1. `theme_list.txt` が正しくpushされているか
2. ファイルが空行だけになっていないか
3. 1行1テーマで書かれているか（余計な改行がないか）

---

## 📝 APIコストについて

### Gemini API（テキスト生成）

- モデル: `gemini-2.0-flash`
- 料金: 現在無料枠あり（2024年12月時点）
- 1記事あたり: 約14セクション生成

### YouTube Data API（Phase2で使用）

- 料金: 1日10,000ユニットまで無料
- 動画情報取得: 1件あたり約3ユニット
- 字幕取得: 無料（YouTube Transcript API使用）

### LINE Notify

- 完全無料

---

## 🎯 次のステップ

### 記事の品質を上げる

- `theme_list.txt` のテーマを具体的にする
- ターゲットペルソナを明確にする（`--target` オプション）

### 本数を増やす

- `theme_list.txt` に追加（1日10本→20本など）
- Gemini APIの無料枠を確認

### 成果物の自動保存

- S3やGoogle Driveへのアップロード機能を追加
- Obsidianへの自動保存機能を追加

---

## 📞 サポート

問題が解決しない場合は、GitHub Issuesで報告してください：
👉 https://github.com/k5k5k5-max/brain-content-system/issues

---

**セットアップ完了です！🎉**

あとはGitHub Actionsが毎日自動でBrain記事を生成してくれます。


