# 📂 ディレクトリ構造定義 Ver.2.0

## Root: `Brain_Content_System_Ver2/`

### 📁 `00_System/`
システムの定義ファイルや運用ルールを格納。
*   `Workflow_Ver2.0.md`: 全体ワークフロー定義書
*   `Directory_Structure.md`: 本ファイル

### 📁 `01_Knowledge/`
ユーザー提供のナレッジや分析フレームワークを格納。
*   `Brain_Analysis_Framework.md`: 売れ筋分析基準
*   `YouTube_Search_Strategy.md`: 動画検索・選定基準
*   `Writing_Style_Okapon.md`: おかぽん式ライティングルール
*   `Design_Concept_Framework.md`: デザインコンセプト定義フレームワーク
*   `Thumbnail_Design_Principles.md`: 情報商材サムネイル特化原則
*   `Prompt_Elements_NanoBanana.md`: 画像生成プロンプト要素定義

### 📁 `02_Templates/`
各工程で使用するテンプレートファイル。
*   `Structure_Template.md`: 構成案のひな形
*   `Sales_Letter_PASONA.md`: セールスレターひな形
*   `Bonus_Content_Template.md`: 特典・LINE誘導ひな形

### 📁 `03_Projects/`
実際のコンテンツ制作プロジェクトを格納するワークスペース。
各プロジェクトは以下の命名規則でフォルダ作成される。
`YYYYMMDD_[テーマ名]/`

#### プロジェクト内部構造 (`YYYYMMDD_[テーマ名]/`)
*   **`01_Research/`**
    *   `market_data.md`: Brain/Tipsのリサーチ結果
    *   `youtube_transcripts/`: 選定動画の字幕データ・要約
    *   `concept_definition.md`: コンセプト定義書（ターゲット、デザイン等）
*   **`02_Planning/`**
    *   `structure_plan.md`: 詳細構成案
    *   `visual_map.md`: 画像配置計画・プロンプト設計図
*   **`03_Content_Draft/`**
    *   `00_Free_Part.md`: 無料パート原稿
    *   `01_Chapter1.md` ~ `05_Chapter5.md`: 各章の原稿
    *   `06_Bonus.md`: 特典パート原稿
*   **`04_Images/`**
    *   `thumbnails/`: メインサムネイル候補
    *   `banners/`: 章見出しバナー画像
    *   `illustrations/`: 記事内挿絵・図解
*   **`05_Final/`**
    *   `Final_Package.md`: 画像とテキストが統合された最終稿
    *   `Description_for_Brain.txt`: プラットフォーム投稿用説明文

---

## 🎨 画像生成ルール（NanoBanana Pro）

### サイズ規定
1.  **メインサムネイル**: `1920x1080` (16:9)
2.  **章見出しバナー**: `1920x1080` (16:9) ※トリミング前提の構図
3.  **挿絵・図解**: `1920x1080` (16:9) または `1024x1024` (1:1)

### ファイル命名規則
*   サムネ: `thumb_v[バージョン]_[識別子].png`
*   バナー: `banner_ch[章番号]_[識別子].png`
*   挿絵: `ill_ch[章番号]_[識別子].png`



