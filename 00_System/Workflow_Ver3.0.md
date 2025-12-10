# Brain Content System Ver3.0 - Workflow

**完全自動化 + Googleドライブ連携版**  
毎日自動で10記事を生成し、Googleドライブに保存、外注さんに通知

---

## 🎯 システム概要

### 目的
- Brain/Tipsでの情報商材販売を目的としたコンテンツを自動生成
- Googleドライブに自動アップロードして外注さんと共有
- LINE通知で完成を即座にお知らせ

### 最終成果物
1. **完成記事（Markdown）**: テキスト + 画像埋め込み済み
2. **投稿用HTML**: Brain/Tips投稿用フォーマット
3. **画像一式**: Googleドライブに自動配置
4. **外注さんへの通知**: LINEでドライブリンクを送信

---

## 🆕 Ver3.0の新機能

### Phase 6: Googleドライブ自動アップロード ★NEW
- 生成した記事と画像を自動的にGoogleドライブにアップロード
- 年月別 → 日付+テーマ別にフォルダ分け
- 外注さんと共有フォルダで即座に受け渡し

### LINE通知の強化 ★NEW
- 各記事完了時にGoogleドライブのリンクを通知
- 文字数・画像数などの統計情報も表示
- バッチ完了時に全記事のサマリーを送信

### GitHub Actions対応 ★NEW
- クラウドで完全自動実行
- Macがスリープ中でも動作
- 毎日定時に自動生成（デフォルト: JST 12:30）

---

## 🔄 6つのPhase

### Phase 1: リサーチ & コンセプト定義
**目的**: テーマの市場性を調査し、記事のコンセプトを決定

**入力**:
- テーマ（例: "Threadsで月5万円稼ぐ方法"）
- ターゲットペルソナ（任意）

**処理**:
1. Brain/Tipsでの類似商品リサーチ（販売数、価格帯、レビュー）
2. ターゲットペルソナ定義
3. 差別化ポイント抽出
4. 価格戦略決定

**出力**:
- `01_Research/concept_definition.md`

---

### Phase 2: ノウハウ抽出
**目的**: YouTubeから実践的なノウハウを収集

**入力**:
- `concept_definition.md`（Phase 1の出力）
- YouTube検索キーワード

**処理**:
1. YouTube動画検索（3-5本）
2. 字幕データ取得
3. LLMでノウハウ抽出（マトリクス形式）
4. 実践テクニックの整理

**出力**:
- `01_Research/knowhow_extraction.md`

**重要ポイント**:
- 発信者名は記載しない（ノウハウのみ抽出）
- 情報密度を高く保つ

---

### Phase 3: 構成設計 & ビジュアル計画
**目的**: DRM構造の記事構成と画像配置を設計

**入力**:
- `knowhow_extraction.md`（Phase 2の出力）
- `concept_definition.md`

**処理**:
1. DRM構造設計（無料パート/有料パート/ボーナス）
2. セクション分割（無料: 3-5、有料: 5-7、ボーナス: 1）
3. 各セクションの目的・内容・文字数を決定
4. 画像配置計画（イラスト/バナー/テキストバナー）
5. Gemini プロンプト作成

**出力**:
- `02_Planning/structure_plan.md`
- `02_Planning/visual_map.md`

---

### Phase 4: 執筆 & 画像生成
**目的**: テキスト執筆と画像生成を実行

**入力**:
- `structure_plan.md`（Phase 3の出力）
- `visual_map.md`
- `knowhow_extraction.md`

**処理**:
1. **テキスト執筆**（Gemini API）
   - 無料パート執筆
   - 有料パート執筆
   - ボーナスパート執筆
   
2. **画像生成**（Gemini Image API）
   - 16:9アスペクト比で生成
   - イラスト + バナー + テキストバナー

**出力**:
- `03_Content_Draft/*.md`
- `04_Images/**/*.png`

---

### Phase 5: 統合 & パッケージング
**目的**: バラバラのファイルを1つの完成記事にまとめる

**入力**:
- `03_Content_Draft/*.md`（全テキストファイル）
- `04_Images/**/*.png`（全画像）
- `02_Planning/visual_map.md`（画像配置情報）

**処理**:
1. テキスト統合
2. 画像埋め込み
3. メタ情報追加
4. HTML変換
5. 画像ZIP化

**出力**:
- `05_Final/final_article.md` ★完成記事（Markdown版）
- `05_Final/final_article.html` ★完成記事（HTML版）
- `05_Final/images.zip` ★画像一式
- `05_Final/metadata.json`（記事情報）

---

### Phase 6: Googleドライブアップロード ★NEW
**目的**: 完成した記事をGoogleドライブに自動アップロード

**入力**:
- `05_Final/`（Phase 5の出力）
- Googleドライブ認証情報
- 共有フォルダID

**処理**:
1. Google Drive API認証
2. 年月フォルダを取得または作成（例: `2024年12月`）
3. テーマフォルダを作成（例: `20241210_Threadsで月5万円稼ぐ方法`）
4. ファイルをアップロード:
   - `final_article.md`
   - `final_article.html`
   - `images/` フォルダ（全画像）

**出力**:
- GoogleドライブURL
- アップロード結果（成功/失敗）

**フォルダ構造**:
```
Brain記事/
└── 2024年12月/
    └── 20241210_Threadsで月5万円稼ぐ方法/
        ├── final_article.md
        ├── final_article.html
        └── images/
            ├── banner_01.png
            ├── ill_01.png
            └── ...
```

---

## 🤖 自動化実行の流れ

### 実行コマンド（ローカル）
```bash
python master_generator.py \
  --theme "Threadsで月5万円稼ぐ方法" \
  --target "副業を始めたい30代会社員" \
  --config test_config.json
```

### バッチ実行（複数テーマ）
```bash
python batch_runner.py \
  --theme-file theme_list.txt \
  --config test_config.json \
  --target "副業初心者の20代会社員"
```

### GitHub Actions自動実行
- **スケジュール**: 毎日 JST 12:30（UTC 03:30）
- **実行内容**:
  1. `theme_list.txt` からテーマを読み込み
  2. 各テーマごとに記事を生成
  3. Googleドライブにアップロード
  4. LINEで通知
- **手動実行**: GitHub Actionsページから「Run workflow」

---

## 📱 LINE通知の内容

### バッチ開始時
```
🟢 Brainバッチ開始: 10件 (batch_id=20241210-123000)
```

### 各記事完了時
```
✅ [1/10] Threadsで月5万円稼ぐ方法
📂 https://drive.google.com/drive/folders/abc123
📝 17,702文字 | 🖼 23枚
```

### バッチ完了時
```
🏁 Brainバッチ完了: 成功10/失敗0

【完成した記事】
✅ Threadsで月5万円稼ぐ方法
   🔗 https://drive.google.com/drive/folders/abc123
✅ ChatGPTで副業を始める方法
   🔗 https://drive.google.com/drive/folders/def456
...
```

---

## 📂 ディレクトリ構造

```
Brain_Content_System_Ver2/
├── 00_System/
│   ├── Workflow_Ver3.0.md（このファイル）
│   ├── master_generator.py（メインスクリプト）
│   ├── batch_runner.py（バッチ処理）
│   ├── test_config.json（設定ファイル）
│   ├── theme_list.txt（テーマリスト）
│   └── modules/
│       ├── phase1_research.py
│       ├── phase2_knowhow.py
│       ├── phase3_structure.py
│       ├── phase4_writing.py
│       ├── phase5_integration.py
│       └── phase6_drive_upload.py ★NEW
├── .github/
│   └── workflows/
│       └── brain_batch.yml（GitHub Actions設定）
├── 03_Projects/
│   └── [YYYYMMDD_ProjectName]/
│       ├── result.json ★NEW（実行結果）
│       ├── 01_Research/
│       │   ├── concept_definition.md
│       │   └── knowhow_extraction.md
│       ├── 02_Planning/
│       │   ├── structure_plan.md
│       │   └── visual_map.md
│       ├── 03_Content_Draft/
│       │   └── *.md
│       ├── 04_Images/
│       │   └── *.png
│       └── 05_Final/
│           ├── final_article.md
│           ├── final_article.html
│           └── images.zip
├── GOOGLE_DRIVE_SETUP.md ★NEW（セットアップガイド）
└── GITHUB_ACTIONS_SETUP.md
```

---

## ⚙️ 設定ファイル（test_config.json）

```json
{
  "youtube_keyword": "Threads 稼ぐ方法",
  "max_youtube_videos": 3,
  "enable_text_generation": true,
  "enable_image_generation": true,
  "prefer_gemini_for_text": true,
  "enable_drive_upload": true,
  "google_drive_folder_id": "1P8RssQ4VfMCmc-cB6NelrAtMKVljNdg_"
}
```

### パラメータ説明

| パラメータ | 説明 | デフォルト |
|----------|------|----------|
| `youtube_keyword` | YouTube検索キーワード | "Threads 稼ぐ方法" |
| `max_youtube_videos` | 取得する動画数 | 3 |
| `enable_text_generation` | テキスト生成を有効化 | true |
| `enable_image_generation` | 画像生成を有効化 | true |
| `prefer_gemini_for_text` | テキスト生成にGeminiを使用 | true |
| `enable_drive_upload` | Googleドライブアップロードを有効化 | true |
| `google_drive_folder_id` | アップロード先フォルダID | （ユーザー提供） |

---

## 🔑 必要なAPIキー

### 必須
1. **GEMINI_API_KEY**: テキスト生成 & 画像生成
2. **LINE_NOTIFY_TOKEN**: LINE通知
3. **GOOGLE_APPLICATION_CREDENTIALS**: Googleドライブアップロード

### 任意
4. **ANTHROPIC_API_KEY**: Claude API（テキスト生成の代替）
5. **YOUTUBE_API_KEY**: YouTube API（Phase 2で字幕取得できない場合）

### 設定方法

#### ローカル環境
```bash
# .envファイルに記載
GEMINI_API_KEY=your_gemini_api_key
LINE_NOTIFY_TOKEN=your_line_notify_token
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

#### GitHub Actions
GitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」で設定

---

## 🎯 運用フロー

### 1日の流れ

```
12:30 JST | GitHub Actions が自動起動
   ↓
12:31     | theme_list.txt から10テーマ読み込み
   ↓
12:32     | 【テーマ1】記事生成開始
   ↓
12:42     | 【テーマ1】Googleドライブにアップロード
   ↓       | LINEに通知（ドライブURL付き）
   ↓
12:43     | 【テーマ2】記事生成開始
   ↓
...       | （以下繰り返し）
   ↓
14:00     | 【テーマ10】完了
   ↓       | LINEに完了サマリー送信
   ↓
14:00     | 外注さんがGoogleドライブから記事をダウンロード
   ↓
14:30     | 外注さんがBrain/Tipsにアップロード
   ↓
15:00     | 販売開始 🎉
```

---

## 📊 コスト試算

### 1記事あたり
- **Gemini API**（テキスト生成）: 無料枠内
- **Gemini API**（画像生成23枚）: 無料枠内
- **Google Drive API**: 無料枠内
- **合計**: ¥0

### 10記事/日
- **月間コスト**: ¥0（無料枠内）
- **月間記事数**: 300記事

---

## 🚀 今後の拡張

### Phase 0: 自動テーマ選定 ★予定
- Brain/Tipsのトレンドを自動スクレイピング
- 売れ筋ジャンルから自動でテーマを選定
- 手動リスト更新が不要に

### コスト最適化
- Gemini API無料枠管理
- 生成済み画像の再利用
- バッチ処理の並列化

### 品質向上
- A/Bテスト機能（複数バージョン生成）
- SEO最適化
- 外注さんからのフィードバック機能

---

## 📝 更新履歴

- **Ver3.0（2024-12-10）**: Googleドライブ連携、LINE通知強化、GitHub Actions対応
- **Ver2.0（2024-12-07）**: 完全自動化対応、Phase 5追加
- **Ver1.0（2024-12-05）**: 初版リリース

