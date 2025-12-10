# Brain Content System Ver2.0 - Workflow

**完全自動化対応版**  
1コマンドでBrain/Tips記事を完成させるシステム

---

## 🎯 システム概要

### 目的
- Brain/Tipsでの情報商材販売を目的としたコンテンツを自動生成
- テキスト執筆 + 画像生成 + 統合パッケージングを一気通貫で実行

### 最終成果物
1. **完成記事（Markdown）**: テキスト + 画像埋め込み済み
2. **投稿用HTML**: Brain/Tips投稿用フォーマット
3. **画像一式（ZIP）**: アップロード用

---

## 🔄 5つのPhase

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
  - テーマ
  - ターゲットペルソナ（年齢、職業、悩み）
  - 提供価値
  - 差別化ポイント
  - 価格戦略（定価、初回限定価格）

---

### Phase 2: ノウハウ抽出
**目的**: YouTubeやWeb記事から実践的なノウハウを収集

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
  - ノウハウマトリクス（動画ごとの比較表）
  - 採用ノウハウ一覧
  - 実践テクニック
  - 注意点・よくある失敗

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
5. NanoBanana プロンプト作成

**出力**:
- `02_Planning/structure_plan.md`
  - 無料パート構成（各セクションの見出し、目的、文字数）
  - 有料パート構成
  - ボーナスパート構成
- `02_Planning/visual_map.md`
  - 画像配置一覧
  - 各画像のNanoBananaプロンプト
  - アスペクト比（16:9推奨）

---

### Phase 4: 執筆 & 画像生成
**目的**: テキスト執筆と画像生成を実行

**入力**:
- `structure_plan.md`（Phase 3の出力）
- `visual_map.md`
- `knowhow_extraction.md`

**処理**:
1. **無料パート執筆**
   - 冒頭に強力なフック（3文）を配置 ★重要
   - 発信者名は一切記載しない ★重要
   - 価格戦略を明示（例: 定価4,980円 → 100円、24時間限定） ★重要
   
2. **有料パート執筆**
   - 各STEPを詳細に執筆
   - 実践的な内容を重視
   
3. **ボーナスパート執筆**
   - 標準3大特典:
     - ① 14日間無制限LINEサポート
     - ② AI活用プロンプト集50選
     - ③ 0→1達成ロードマップ（30日版）
   
4. **画像生成**
   - NanoBanana Pro（Gemini API）使用
   - **16:9アスペクト比を厳守** ★重要
   - プロンプトに "16:9 landscape, 1376x768 resolution" を明記
   - 日本語テキストを含める
   - イラスト + バナー + テキストバナーを生成
   
5. **テキストバナー追加** ★重要
   - 無料パートに5枚程度追加
   - セールス訴求を強化

**出力**:
- `03_Content_Draft/00_Free_Part.md`
- `03_Content_Draft/01_Paid_Part_Intro_Step1.md`
- `03_Content_Draft/02_Paid_Part_Step2.md`
- `03_Content_Draft/03_Paid_Part_Step3.md`
- `03_Content_Draft/04_Paid_Part_Step4.md`
- `03_Content_Draft/05_Paid_Part_Step5.md`
- `03_Content_Draft/06_Paid_Part_Conclusion.md`
- `04_Images/illustrations/*.png`（16:9）
- `04_Images/banners/*.png`（16:9）
- `04_Images/text_banners/*.png`（16:9）
- `04_Images/bonus_thumbnails/*.png`（16:9、情報商材特化デザイン）

**ボーナスサムネイル仕様** ★重要:
- 情報商材サムネイル特化デザイン原則に従う
- 三層構造レイアウト（上段: 特典番号、中央: メインタイトル、下段: ベネフィット）
- 色味を3つとも変える（例: Gold×Black、Silver×DeepBlue、RoseGold×Purple）
- 3Dメタリック質感の太字ゴシック体
- 購入者限定追加特典①②③を明記

---

### Phase 5: 統合 & パッケージング ★新規
**目的**: バラバラのファイルを1つの完成記事にまとめる

**入力**:
- `03_Content_Draft/*.md`（全テキストファイル）
- `04_Images/**/*.png`（全画像）
- `02_Planning/visual_map.md`（画像配置情報）

**処理**:
1. **テキスト統合**
   - 無料パート → 有料パート → ボーナスパートを結合
   - セクション間に適切な区切りを挿入
   
2. **画像埋め込み**
   - visual_map.mdに従って画像を適切な位置に配置
   - Markdown形式: `![説明](相対パス)`
   - HTML形式: `<img src="相対パス" alt="説明" />`
   
3. **メタ情報追加**
   - タイトル
   - 価格情報
   - 特典一覧
   - 購入リンク（LINE登録）
   
4. **HTML変換**
   - Brain/Tips投稿用HTMLを生成
   - スタイル適用（見出し、リスト、画像）
   
5. **画像ZIP化**
   - 全画像を1つのZIPファイルにまとめる
   - ファイル名をわかりやすく整理

**出力**:
- `05_Final/final_article.md` ★完成記事（Markdown版）
- `05_Final/final_article.html` ★完成記事（HTML版）
- `05_Final/images.zip` ★画像一式
- `05_Final/metadata.json`（記事情報: タイトル、価格、画像数など）

---

## 🤖 自動化実行の流れ

### 実行コマンド
```bash
python master_generator.py --theme "Threadsで月5万円稼ぐ方法" --target "副業を始めたい30代会社員"
```

### 実行ログ（例）
```
🚀 Brain Content System Ver2.0 起動
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 設定確認:
  テーマ: Threadsで月5万円稼ぐ方法
  ターゲット: 副業を始めたい30代会社員
  プロジェクト: 20241207_Threads_Income

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Phase 1] リサーチ & コンセプト定義
  ├─ Brain/Tipsリサーチ中... ✅ 完了（15件取得）
  ├─ ペルソナ定義中... ✅ 完了
  └─ コンセプト定義完了
  📁 concept_definition.md 保存完了

[Phase 2] ノウハウ抽出
  ├─ YouTube検索中... ✅ 完了（5件取得）
  ├─ 字幕取得中... ✅ 完了
  ├─ ノウハウ抽出中（Claude API）... ✅ 完了
  └─ ノウハウ整理完了
  📁 knowhow_extraction.md 保存完了

[Phase 3] 構成設計 & ビジュアル計画
  ├─ DRM構造設計中... ✅ 完了
  ├─ 画像配置計画中... ✅ 完了
  └─ NanoBananaプロンプト生成完了
  📁 structure_plan.md 保存完了
  📁 visual_map.md 保存完了

[Phase 4] 執筆 & 画像生成
  ├─ 無料パート執筆中（Claude API）... ✅ 完了（3,245文字）
  ├─ 有料パート執筆中（5セクション）... ✅ 完了（12,890文字）
  ├─ ボーナスパート執筆中... ✅ 完了（1,567文字）
  ├─ 画像生成中（1/23: メインサムネイル）... ✅ 完了
  ├─ 画像生成中（2/23: 無料パートイラスト1）... ✅ 完了
  ...
  └─ 画像生成中（23/23: ボーナスサムネイル3）... ✅ 完了
  📁 全テキスト保存完了
  📁 全画像保存完了（23枚）

[Phase 5] 統合 & パッケージング
  ├─ テキスト統合中... ✅ 完了（17,702文字）
  ├─ 画像埋め込み中... ✅ 完了（23枚配置）
  ├─ HTML変換中... ✅ 完了
  └─ ZIP圧縮中... ✅ 完了（23枚、4.2MB）
  📁 final_article.md 保存完了
  📁 final_article.html 保存完了
  📁 images.zip 保存完了

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 記事生成完了！

📊 統計情報:
  総文字数: 17,702文字
  画像数: 23枚
  所要時間: 8分32秒
  
  Claude API使用量:
    入力: 83,245トークン ($0.250)
    出力: 29,412トークン ($0.441)
  
  Gemini API使用量:
    画像生成: 23枚 (無料枠内)

💰 今回のコスト: $0.691 ≈ ¥108

📁 成果物:
  ✅ 05_Final/final_article.md
  ✅ 05_Final/final_article.html
  ✅ 05_Final/images.zip

🚀 次のステップ:
  1. final_article.htmlをBrainにアップロード
  2. images.zipを解凍して画像を配置
  3. 価格設定（推奨: 4,980円 → 100円 24時間限定）
  4. LINE登録リンクを設定

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📂 ディレクトリ構造

```
Brain_Content_System_Ver2/
├── 00_System/
│   ├── Workflow_Ver2.0.md（このファイル）
│   ├── master_generator.py（メインスクリプト）
│   └── modules/
│       ├── __init__.py
│       ├── phase1_research.py
│       ├── phase2_knowhow.py
│       ├── phase3_structure.py
│       ├── phase4_writing.py
│       ├── phase5_integration.py
│       ├── image_generator.py
│       └── utils.py
├── 01_Knowledge/
│   └── Brain_Content_Creation_Knowledge.md
└── 03_Projects/
    └── [YYYYMMDD_ProjectName]/
        ├── config.json（プロジェクト設定）
        ├── 01_Research/
        │   ├── concept_definition.md
        │   ├── knowhow_extraction.md
        │   └── competitor_analysis.md
        ├── 02_Planning/
        │   ├── structure_plan.md
        │   └── visual_map.md
        ├── 03_Content_Draft/
        │   ├── 00_Free_Part.md
        │   ├── 01_Paid_Part_Intro_Step1.md
        │   ├── 02_Paid_Part_Step2.md
        │   ├── 03_Paid_Part_Step3.md
        │   ├── 04_Paid_Part_Step4.md
        │   ├── 05_Paid_Part_Step5.md
        │   └── 06_Paid_Part_Conclusion.md
        ├── 04_Images/
        │   ├── illustrations/
        │   ├── banners/
        │   ├── text_banners/
        │   └── bonus_thumbnails/
        └── 05_Final/
            ├── final_article.md ★最終成果物
            ├── final_article.html
            ├── images.zip
            └── metadata.json
```

---

## 🎯 今後の拡張

### 1日10記事自動生成への対応
- バッチ処理機能追加
- テーマリスト読み込み
- 並列処理対応
- エラーリトライ機能

### コスト最適化
- Gemini API無料枠管理
- Claude APIキャッシング活用
- 生成済み画像の再利用

### 品質向上
- レビュー機能（人間確認）
- A/Bテスト機能（複数バージョン生成）
- SEO最適化

---

## 📝 更新履歴

- **Ver2.0（2024-12-07）**: 完全自動化対応、Phase 5追加
- **Ver1.0（2024-12-05）**: 初版リリース
