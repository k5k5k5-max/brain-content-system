#!/usr/bin/env python3
"""
Phase 3: 構成設計 & ビジュアル計画
ノウハウとコンセプトから最適な記事構成を自動生成
"""

from pathlib import Path
import anthropic
import os
import json


# Gemini API
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def load_claude_api_key():
    """Claude APIキーを読み込む"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        return api_key.strip()
    
    env_paths = [
        Path("/Users/keigo/001_cursor/.env"),
        Path("/Users/keigo/001_cursor/文字起こしブースター/mioji_share_v2/.env"),
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key == "ANTHROPIC_API_KEY":
                                return value.strip()
            except Exception:
                continue
    
    return None


def load_gemini_api_key():
    """Gemini APIキーを読み込む"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        return api_key.strip()
    
    env_paths = [
        Path("/Users/keigo/001_cursor/.env"),
        Path("/Users/keigo/001_cursor/文字起こしブースター/mioji_share_v2/.env"),
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key == "GEMINI_API_KEY":
                                return value.strip()
            except Exception:
                continue
    
    return None


def generate_structure_plan(knowhow_content, concept_content, claude_client):
    """Claude APIで構成プランを生成"""
    prompt = f"""あなたはプロのコンテンツ設計者です。以下の情報をもとに、Brain/Tips向けの記事構成を設計してください。

【参考ノウハウ】
{knowhow_content[:3000]}  # 長すぎる場合は切り詰め

【コンセプト】
{concept_content}

【タスク】
以下のフォーマットで記事構成を設計してください：

1. **無料パート**（5-8セクション）
   - 読者の興味を引き、有料パートへ誘導する
   - セクションごとに：見出し、目的、文字数目安、必要な画像

2. **有料パート**（5-7セクション/STEP）
   - 実践的なノウハウを段階的に提供
   - 各STEPごとに：見出し、目的、文字数目安、必要な画像

3. **ボーナスパート**（1セクション）
   - 購入者限定特典（LINE登録誘導）
   - 標準3大特典：
     - ① 14日間無制限LINEサポート
     - ② AI活用プロンプト集50選
     - ③ 0→1達成ロードマップ（30日版）

【画像の種類】
- イラスト（ill_*.png）: 概念図、フロー図、ビフォーアフターなど
- バナー（banner_*.png）: セクション見出し画像
- テキストバナー（text_banner_*.png）: 強調訴求、データ、価格など
- ボーナスサムネイル（bonus_thumb_*.png）: 特典サムネイル

【出力フォーマット】
以下のJSON形式で出力してください：

```json
{{
  "free_sections": [
    {{
      "title": "セクション見出し",
      "purpose": "このセクションの目的",
      "chars": "文字数目安（例: 800-1000）",
      "images": [
        {{"filename": "ill_example.png", "type": "イラスト", "description": "画像の内容説明", "position": "後"}}
      ]
    }}
  ],
  "paid_sections": [
    {{
      "title": "STEP 1: タイトル",
      "purpose": "このSTEPの目的",
      "chars": "文字数目安",
      "images": [...]
    }}
  ],
  "bonus_section": {{
    "title": "購入者限定追加特典",
    "purpose": "LINE登録誘導",
    "chars": "500-700",
    "images": [
      {{"filename": "bonus_thumb_01_line_support.png", "type": "サムネイル", "description": "14日間無制限LINEサポート", "position": "後"}},
      {{"filename": "bonus_thumb_02_ai_prompts.png", "type": "サムネイル", "description": "AI活用プロンプト集50選", "position": "後"}},
      {{"filename": "bonus_thumb_03_roadmap.png", "type": "サムネイル", "description": "0→1達成ロードマップ", "position": "後"}}
    ]
  }}
}}
```

JSONのみを出力してください（説明文は不要）。
"""
    
    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        text = response.content[0].text
        
        # JSONを抽出（```json ... ``` の中身）
        if "```json" in text:
            json_start = text.find("```json") + 7
            json_end = text.find("```", json_start)
            json_text = text[json_start:json_end].strip()
        elif "```" in text:
            json_start = text.find("```") + 3
            json_end = text.find("```", json_start)
            json_text = text[json_start:json_end].strip()
        else:
            json_text = text.strip()
        
        structure_data = json.loads(json_text)
        
        return structure_data, response.usage.input_tokens, response.usage.output_tokens
    
    except Exception as e:
        print(f"    ❌ エラー: {str(e)}")
        return None, 0, 0



def generate_structure_with_gemini(knowhow_content, concept_content, gemini_client):
    """Gemini APIで構成プランを生成"""
    prompt = f"""あなたはプロのコンテンツ設計者です。以下のノウハウとコンセプトから、Brain/Tips向けの最適な記事構成を設計してください。

【ノウハウ】
{knowhow_content}

【コンセプト】
{concept_content}

【タスク】
以下のフォーマットで記事構成を設計してください：

1. **無料パート**（5-8セクション）
   - 読者の興味を引き、有料パートへ誘導する
   - セクションごとに：見出し、目的、文字数目安、必要な画像

2. **有料パート**（5-7セクション/STEP）
   - 実践的なノウハウを段階的に提供
   - 各STEPごとに：見出し、目的、文字数目安、必要な画像

3. **ボーナスパート**（1セクション）
   - 購入者限定特典（LINE登録誘導）
   - 標準3大特典：
     - ① 14日間無制限LINEサポート
     - ② AI活用プロンプト集50選
     - ③ 0→1達成ロードマップ（30日版）

【画像の種類】
- イラスト（ill_*.png）: 概念図、フロー図、ビフォーアフターなど
- バナー（banner_*.png）: セクション見出し画像
- テキストバナー（text_banner_*.png）: 強調訴求、データ、価格など
- ボーナスサムネイル（bonus_thumb_*.png）: 特典サムネイル

【出力フォーマット】
以下のJSON形式で出力してください：

```json
{{
  "free_sections": [
    {{
      "title": "セクション見出し",
      "purpose": "このセクションの目的",
      "chars": "文字数目安（例: 800-1000）",
      "images": [
        {{"filename": "ill_example.png", "type": "イラスト", "description": "画像の内容説明", "position": "後"}}
      ]
    }}
  ],
  "paid_sections": [
    {{
      "title": "STEP 1: タイトル",
      "purpose": "このSTEPの目的",
      "chars": "文字数目安",
      "images": [...]
    }}
  ],
  "bonus_section": {{
    "title": "購入者限定追加特典",
    "purpose": "LINE登録誘導",
    "chars": "500-700",
    "images": [
      {{"filename": "bonus_thumb_01_line_support.png", "type": "サムネイル", "description": "14日間無制限LINEサポート", "position": "後"}},
      {{"filename": "bonus_thumb_02_ai_prompts.png", "type": "サムネイル", "description": "AI活用プロンプト集50選", "position": "後"}},
      {{"filename": "bonus_thumb_03_roadmap.png", "type": "サムネイル", "description": "0→1達成ロードマップ", "position": "後"}}
    ]
  }}
}}
```

JSONのみを出力してください（説明文は不要）。
"""
    
    try:
        response = gemini_client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=prompt
        )
        text = response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text
        
        # JSONを抽出（```json ... ``` の中身）
        if "```json" in text:
            json_start = text.find("```json") + 7
            json_end = text.find("```", json_start)
            json_text = text[json_start:json_end].strip()
        elif "```" in text:
            json_start = text.find("```") + 3
            json_end = text.find("```", json_start)
            json_text = text[json_start:json_end].strip()
        else:
            json_text = text.strip()
        
        structure_data = json.loads(json_text)
        
        return structure_data, 0, 0  # Geminiのトークン情報は未集計
    
    except Exception as e:
        print(f"    ❌ Geminiエラー: {str(e)}")
        return None, 0, 0


def format_structure_plan_md(structure_data):
    """構成データをstructure_plan.mdのフォーマットに変換"""
    lines = [
        "# 構成プラン",
        "",
        "## 無料パート",
        ""
    ]
    
    # 無料パート
    for i, section in enumerate(structure_data.get("free_sections", []), 1):
        lines.append(f"### セクション{i}: {section['title']}")
        lines.append(f"- **目的**: {section['purpose']}")
        lines.append(f"- **文字数**: {section['chars']}文字")
        
        if section.get('images'):
            lines.append("- **画像**:")
            for img in section['images']:
                lines.append(f"  - {img['filename']}（{img['type']}、配置位置: {img['position']}）")
        else:
            lines.append("- **画像**: なし")
        
        lines.append("")
    
    # 有料パート
    lines.append("---")
    lines.append("")
    lines.append("## 有料パート")
    lines.append("")
    
    for section in structure_data.get("paid_sections", []):
        lines.append(f"### {section['title']}")
        lines.append(f"- **目的**: {section['purpose']}")
        lines.append(f"- **文字数**: {section['chars']}文字")
        
        if section.get('images'):
            lines.append("- **画像**:")
            for img in section['images']:
                lines.append(f"  - {img['filename']}（{img['type']}、配置位置: {img['position']}）")
        else:
            lines.append("- **画像**: なし")
        
        lines.append("")
    
    # ボーナスパート
    if structure_data.get("bonus_section"):
        bonus = structure_data["bonus_section"]
        lines.append("---")
        lines.append("")
        lines.append("## ボーナスパート")
        lines.append("")
        lines.append(f"### {bonus['title']}")
        lines.append(f"- **目的**: {bonus['purpose']}")
        lines.append(f"- **文字数**: {bonus['chars']}文字")
        
        if bonus.get('images'):
            lines.append("- **画像**:")
            for img in bonus['images']:
                lines.append(f"  - {img['filename']}（{img['type']}、配置位置: {img['position']}）")
        
        lines.append("")
    
    return "\n".join(lines)


def run(project_dir, prefer_gemini=True):
    """Phase 3実行"""
    # APIキー読み込み
    gemini_key = load_gemini_api_key() if prefer_gemini else None
    claude_key = load_claude_api_key() if not prefer_gemini else None
    
    # Gemini優先、なければClaude
    if prefer_gemini:
        if gemini_key and GEMINI_AVAILABLE:
            print("  ├─ Gemini APIキー読み込み中...")
            print("  │  └─ Gemini APIキー: OK")
            use_gemini = True
        else:
            print("  ├─ Gemini APIキーが見つかりません。Claudeを試します...")
            claude_key = load_claude_api_key()
            if not claude_key:
                print("  ⚠️  Claude APIキーも見つかりません")
                return None
            print("  │  └─ Claude APIキー: OK")
            use_gemini = False
    else:
        print("  ├─ Claude APIキー読み込み中...")
        if not claude_key:
            print("  ⚠️  Claude APIキーが見つかりません")
            return None
        print("  │  └─ Claude APIキー: OK")
        use_gemini = False
    
    # ノウハウとコンセプトを読み込み
    print("  ├─ ノウハウ & コンセプト読み込み中...")
    knowhow_file = project_dir / "01_Research" / "knowhow_extraction.md"
    concept_file = project_dir / "01_Research" / "concept_definition.md"
    
    if not knowhow_file.exists() or not concept_file.exists():
        print("  ⚠️  必要なファイルが見つかりません")
        return None
    
    knowhow_content = knowhow_file.read_text(encoding="utf-8")
    concept_content = concept_file.read_text(encoding="utf-8")
    
    print("  │  └─ ノウハウ: OK")
    print("  │  └─ コンセプト: OK")
    
    # 構成プラン生成
    print("  ├─ 構成プラン生成中（Claude API）...")
    structure_data, input_tokens, output_tokens = generate_structure_plan(
        knowhow_content, concept_content, claude_client
    )
    
    if not structure_data:
        print("  ⚠️  構成プラン生成失敗")
        return None
    
    free_count = len(structure_data.get("free_sections", []))
    paid_count = len(structure_data.get("paid_sections", []))
    print(f"  │  └─ 無料パート: {free_count}セクション")
    print(f"  │  └─ 有料パート: {paid_count}セクション")
    
    # structure_plan.md を生成
    print("  ├─ structure_plan.md 生成中...")
    planning_dir = project_dir / "02_Planning"
    planning_dir.mkdir(parents=True, exist_ok=True)
    
    structure_file = planning_dir / "structure_plan.md"
    structure_md = format_structure_plan_md(structure_data)
    structure_file.write_text(structure_md, encoding="utf-8")
    
    print(f"  │  └─ {structure_file.name} 保存完了")
    
    print("  └─ Phase 3完了")
    
    return {
        "structure_file": str(structure_file),
        "free_sections": free_count,
        "paid_sections": paid_count,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }

