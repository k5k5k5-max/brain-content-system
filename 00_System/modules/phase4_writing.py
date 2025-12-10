#!/usr/bin/env python3
"""
Phase 4: 執筆 & 画像生成
テキスト執筆、画像生成、visual_map.md自動生成
"""

from pathlib import Path
import re
import os
import anthropic
from google import genai


def parse_structure_plan(structure_file):
    """structure_plan.md を解析して画像配置情報とセクション情報を抽出"""
    if not structure_file.exists():
        return {}
    
    content = structure_file.read_text(encoding="utf-8")
    
    # セクションごとの画像情報とメタデータ
    sections = {}
    
    current_section = None
    current_images = []
    current_purpose = "情報提供"
    current_chars = "800-1000"
    
    lines = content.split("\n")
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # セクション見出しを検出（### で始まる行）
        if line.startswith("### "):
            # 前のセクションを保存
            if current_section:
                sections[current_section] = {
                    "images": current_images,
                    "purpose": current_purpose,
                    "chars": current_chars
                }
            
            # 新しいセクション
            section_name = line[4:].strip()
            # セクション番号を除去（例: "セクション1: " → ""）
            if ":" in section_name:
                section_name = section_name.split(":", 1)[1].strip()
            
            current_section = section_name
            current_images = []
            current_purpose = "情報提供"
            current_chars = "800-1000"
        
        # 目的を検出
        elif line.startswith("- **目的**:") or line.startswith("- **目的**："):
            purpose_text = re.sub(r'^- \*\*目的\*\*[：:]\s*', '', line)
            current_purpose = purpose_text
        
        # 文字数を検出
        elif line.startswith("- **文字数**:") or line.startswith("- **文字数**："):
            chars_text = re.sub(r'^- \*\*文字数\*\*[：:]\s*', '', line)
            chars_text = chars_text.replace("文字", "").strip()
            current_chars = chars_text
        
        # 画像情報を検出（行頭ハイフン + .png を含む行）
        # strip() 済みなので先頭のスペースは消えている点に注意
        elif line.startswith("- ") and ".png" in line:
            # 画像ファイル名と配置位置を抽出
            # 例: "  - text_banner_free_hook.png（テキストバナー、配置位置: 後）"
            
            # ファイル名を抽出
            match = re.search(r'([a-zA-Z0-9_]+\.png)', line)
            if match:
                filename = match.group(1)
                
                # 配置位置を抽出
                position = "後"  # デフォルト
                if "配置位置:" in line or "配置位置：" in line:
                    pos_match = re.search(r'配置位置[：:]\s*([前中後])', line)
                    if pos_match:
                        position = pos_match.group(1)
                
                current_images.append({
                    "file": filename,
                    "position": position
                })
        
        i += 1
    
    # 最後のセクションを保存
    if current_section:
        sections[current_section] = {
            "images": current_images,
            "purpose": current_purpose,
            "chars": current_chars
        }
    
    return sections


def generate_visual_map(sections, output_file):
    """画像配置情報からvisual_map.mdを自動生成"""
    print(f"    🔍 DEBUG: generate_visual_map受信 - {len(sections)}セクション")
    for name, images in list(sections.items())[:3]:
        print(f"      - {name}: {len(images)}枚")
    
    content = [
        "# ビジュアルマップ",
        "",
        "このファイルは、Phase 4で自動生成されました。",
        "記事内の画像配置を定義します。",
        "",
        "## フォーマット説明",
        "",
        "```",
        "### [セクション見出し]（配置位置）",
        "- 画像ファイル名.png",
        "```",
        "",
        "**配置位置**:",
        "- `（前）`: セクションの見出しの直後",
        "- `（後）`: セクションの内容の直後",
        "- `（中）`: セクションの途中（デフォルト）",
        "",
        "---",
        ""
    ]
    
    # セクションごとにグループ化（無料パート、有料パート、ボーナスパート）
    free_sections = {}
    paid_sections = {}
    bonus_sections = {}
    
    for section_name, images in sections.items():
        print(f"    🔍 DEBUG: セクション「{section_name}」処理中 - type={type(images)}, len={len(images) if isinstance(images, list) else 'N/A'}")
        # セクション名から分類
        if any(keyword in section_name for keyword in ["特典", "ボーナス", "購入者限定"]):
            bonus_sections[section_name] = images
        elif any(keyword in section_name for keyword in ["STEP", "イントロダクション", "結論"]):
            paid_sections[section_name] = images
        else:
            free_sections[section_name] = images
    
    # 無料パート
    if free_sections:
        content.append("## 無料パート")
        content.append("")
        for section_name, images in free_sections.items():
            position = images[0]["position"] if images else "後"
            content.append(f"### {section_name}（{position}）")
            for img in images:
                content.append(f"- {img['file']}")
            content.append("")
    
    # 有料パート
    if paid_sections:
        content.append("---")
        content.append("")
        content.append("## 有料パート")
        content.append("")
        for section_name, images in paid_sections.items():
            position = images[0]["position"] if images else "後"
            content.append(f"### {section_name}（{position}）")
            for img in images:
                content.append(f"- {img['file']}")
            content.append("")
    
    # ボーナスパート
    if bonus_sections:
        content.append("---")
        content.append("")
        content.append("## ボーナスパート（最後に追加）")
        content.append("")
        for section_name, images in bonus_sections.items():
            position = images[0]["position"] if images else "後"
            content.append(f"### {section_name}（{position}）")
            for img in images:
                content.append(f"- {img['file']}")
            content.append("")
    
    # ファイルに書き込み
    output_file.write_text("\n".join(content), encoding="utf-8")
    
    return output_file


def load_api_keys():
    """APIキーを環境変数または.envファイルから読み込む"""
    # Claude API Key
    claude_key = os.environ.get('ANTHROPIC_API_KEY')
    if not claude_key:
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
                                    claude_key = value.strip()
                                    break
                except Exception:
                    continue
            if claude_key:
                break
    
    # Gemini API Key
    gemini_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if not gemini_key:
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
                                if key in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]:
                                    gemini_key = value.strip()
                                    break
                except Exception:
                    continue
            if gemini_key:
                break
    
    return claude_key, gemini_key


def generate_text_with_claude(section_name, section_info, knowhow_content, concept_content, claude_client):
    """Claude APIでテキストを生成"""
    # プロンプト構築
    prompt = f"""あなたはプロのコンテンツライターです。以下の情報をもとに、Brain/Tips向けの記事の一部を執筆してください。

【セクション名】
{section_name}

【目的】
{section_info.get('purpose', '情報提供')}

【文字数】
{section_info.get('chars', '800-1000')}文字

【参考ノウハウ】
{knowhow_content}

【コンセプト】
{concept_content}

【執筆ルール】
1. **必ず最初の見出しには、指定されたセクション名「{section_name}」をそのまま使用してください**
2. 見出しは ## {section_name} という形式で開始してください
3. セクション名は一字一句変更せず、完全に同じものを使用してください
4. 読者に寄り添う、わかりやすい文章で書く
5. 具体例を交えて説明する
6. 実践的な内容を重視する
7. サブ見出しは ### を使う
8. リストや箇条書きを適宜使用する
9. 発信者名や他のクリエイター名は一切記載しない

【重要】
記事の最初の見出しは必ず「## {section_name}」で始めてください。セクション名を変更したり、言い換えたりしないでください。

それでは執筆を開始してください。
"""
    
    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        text = response.content[0].text
        return text, response.usage.input_tokens, response.usage.output_tokens
    
    except Exception as e:
        print(f"    ❌ エラー: {str(e)}")
        return None, 0, 0


def generate_text_with_gemini(section_name, section_info, knowhow_content, concept_content, gemini_client):
    """Gemini APIでテキストを生成（Claude代替）"""
    prompt = f"""あなたはプロのコンテンツライターです。以下の情報をもとに、Brain/Tips向けの記事の一部を執筆してください。

【セクション名】
{section_name}

【目的】
{section_info.get('purpose', '情報提供')}

【文字数】
{section_info.get('chars', '800-1000')}文字

【参考ノウハウ】
{knowhow_content}

【コンセプト】
{concept_content}

【執筆ルール】
1. 最初の見出しは必ず「## {section_name}」で始める（名称は一字一句変更しない）
2. 読者に寄り添う、わかりやすい文章で書く
3. 具体例を交えて説明する
4. 実践的な内容を重視する
5. サブ見出しは ### を使う
6. リストや箇条書きを適宜使用する
7. 発信者名や他のクリエイター名は一切記載しない

それでは執筆を開始してください。"""

    try:
        response = gemini_client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=prompt
        )
        text = response.text if hasattr(response, "text") else None
        return text, 0, 0  # Geminiのトークン情報は未集計
    except Exception as e:
        print(f"    ❌ Geminiエラー: {str(e)}")
        return None, 0, 0


def generate_image_with_gemini(image_filename, section_name, gemini_client):
    """Gemini APIで画像を生成"""
    print(f"        🔍 generate_image_with_gemini: {image_filename}")
    
    # 画像タイプを判定
    if "text_banner_" in image_filename:
        image_type = "テキストバナー"
    elif "ill_" in image_filename:
        image_type = "イラスト"
    elif "banner_" in image_filename:
        image_type = "バナー"
    elif "bonus_" in image_filename:
        image_type = "ボーナスサムネイル"
    else:
        image_type = "イラスト"
    
    # プロンプト生成
    prompt = f"""Create a professional image for a digital content article.

Image Type: {image_type}
Section: {section_name}
Filename: {image_filename}

Requirements:
- 16:9 landscape aspect ratio, 1376x768 resolution
- Modern, clean design
- Japanese text should be clear and readable
- High contrast for mobile viewing
- Professional marketing aesthetic

Style:
- If text banner: Bold typography, high impact design
- If illustration: Clean, modern infographic style
- If bonus thumbnail: Three-layer structure with metallic 3D text

IMPORTANT: Output in 16:9 landscape format, 1376x768 pixels.
"""
    
    try:
        print(f"        📡 API呼び出し: model=gemini-3-pro-image-preview")
        response = gemini_client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt
        )
        print(f"        ✅ API呼び出し成功")
        
        # 画像データを取得
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                image_data = part.inline_data.data
                                print(f"        ✅ 画像データ取得: {len(image_data)} bytes")
                                return image_data
        
        print(f"        ⚠️  画像データが見つかりませんでした")
        return None
    
    except Exception as e:
        print(f"        ❌ API エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def run(project_dir, enable_text_generation=True, enable_image_generation=True, prefer_gemini_for_text=False):
    """Phase 4実行"""
    print("  ├─ APIキー読み込み中...")
    claude_key, gemini_key = load_api_keys()
    
    if not claude_key:
        print("  ⚠️  Claude APIキーが見つかりません")
    else:
        print("  │  └─ Claude APIキー: OK")
    
    if not gemini_key:
        print("  ⚠️  Gemini APIキーが見つかりません")
        enable_image_generation = False
    else:
        print("  │  └─ Gemini APIキー: OK")
    
    # Claude/Geminiクライアント初期化
    claude_client = anthropic.Anthropic(api_key=claude_key) if claude_key else None
    gemini_client = genai.Client(api_key=gemini_key, http_options={"api_version": "v1"}) if gemini_key else None

    # テキスト生成クライアントの決定
    use_gemini_for_text = prefer_gemini_for_text or (not claude_client and gemini_client)
    text_client_name = "Gemini" if use_gemini_for_text else "Claude"
    if enable_text_generation:
        if use_gemini_for_text and not gemini_client:
            print("  ⚠️  Geminiクライアント未初期化のためテキスト生成をスキップ")
            enable_text_generation = False
        elif (not use_gemini_for_text) and (not claude_client):
            print("  ⚠️  Claudeクライアント未初期化のためテキスト生成をスキップ")
            enable_text_generation = False
    
    print("  ├─ structure_plan.md 読み込み中...")
    structure_file = project_dir / "02_Planning" / "structure_plan.md"
    
    if not structure_file.exists():
        print("  ⚠️  structure_plan.md が見つかりません")
        return None
    
    # 画像配置情報を抽出
    sections = parse_structure_plan(structure_file)
    print(f"  │  └─ {len(sections)}セクション取得")
    
    # ノウハウとコンセプトを読み込み
    knowhow_file = project_dir / "01_Research" / "knowhow_extraction.md"
    concept_file = project_dir / "01_Research" / "concept_definition.md"
    
    knowhow_content = knowhow_file.read_text(encoding="utf-8") if knowhow_file.exists() else ""
    concept_content = concept_file.read_text(encoding="utf-8") if concept_file.exists() else ""
    
    # テキスト生成
    total_input_tokens = 0
    total_output_tokens = 0
    text_files_created = 0
    
    if enable_text_generation:
        print(f"  ├─ テキスト生成中（{text_client_name} API）...")
        draft_dir = project_dir / "03_Content_Draft"
        draft_dir.mkdir(parents=True, exist_ok=True)
        
        for i, (section_name, section_data) in enumerate(sections.items(), 1):
            print(f"  │  ├─ [{i}/{len(sections)}] {section_name}")
            
            # セクション情報を取得
            section_info = {
                "purpose": section_data.get("purpose", "情報提供"),
                "chars": section_data.get("chars", "800-1000")
            }
            
            if use_gemini_for_text:
                text, input_tokens, output_tokens = generate_text_with_gemini(
                    section_name, section_info, knowhow_content, concept_content, gemini_client
                )
            else:
                text, input_tokens, output_tokens = generate_text_with_claude(
                    section_name, section_info, knowhow_content, concept_content, claude_client
                )
            
            if text:
                # ファイル名を生成
                filename = f"{i:02d}_{section_name.replace(' ', '_').replace('：', '_').replace(':', '_')[:30]}.md"
                output_file = draft_dir / filename
                output_file.write_text(text, encoding="utf-8")
                
                total_input_tokens += input_tokens
                total_output_tokens += output_tokens
                text_files_created += 1
                print(f"  │  │  └─ ✅ {filename} ({len(text)}文字)")
            else:
                print(f"  │  │  └─ ⚠️  生成失敗")
        
        print(f"  │  └─ {text_files_created}ファイル生成完了")
    
    # visual_map.md を自動生成
    print("  ├─ visual_map.md 自動生成中...")
    visual_map_file = project_dir / "02_Planning" / "visual_map.md"
    # sectionsから画像情報のみを抽出
    sections_for_visual_map = {name: data["images"] for name, data in sections.items()}
    
    # デバッグ: 画像情報を確認
    total_images = sum(len(images) for images in sections_for_visual_map.values())
    print(f"  │  🔍 DEBUG: {len(sections_for_visual_map)}セクション、合計{total_images}枚の画像")
    
    generate_visual_map(sections_for_visual_map, visual_map_file)
    print(f"  │  └─ {visual_map_file.name} 保存完了")
    
    # 画像生成
    images_created = 0
    
    print(f"\n  🔍 DEBUG: enable_image_generation={enable_image_generation}")
    print(f"  🔍 DEBUG: gemini_client={gemini_client is not None}")
    print(f"  🔍 DEBUG: sections count={len(sections)}")
    
    if enable_image_generation and gemini_client:
        print("  ├─ 画像生成中（Gemini API）...")
        images_dir = project_dir / "04_Images"
        
        # 画像リストを確認
        total_images = sum(len(data["images"]) for data in sections.values())
        print(f"  │  └─ 生成予定画像数: {total_images}枚")
        
        for section_name, section_data in sections.items():
            images = section_data["images"]
            if not images:
                continue
            print(f"  │  ├─ セクション「{section_name}」: {len(images)}枚")
            
            for img_info in images:
                filename = img_info['file']
                print(f"  │  │  ├─ 処理中: {filename}")
                
                # 画像カテゴリを判定
                if "ill_" in filename:
                    category = "illustrations"
                elif "banner_" in filename:
                    category = "banners"
                elif "text_banner_" in filename:
                    category = "text_banners"
                elif "bonus_" in filename:
                    category = "bonus_thumbnails"
                else:
                    category = "illustrations"
                
                output_dir = images_dir / category
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / filename
                
                # 既に存在する場合はスキップ
                if output_file.exists():
                    print(f"  │  ├─ ⏭️  {filename} (既存)")
                    continue
                
                print(f"  │  │  ├─ 🎨 生成開始: {filename}")
                
                try:
                    image_data = generate_image_with_gemini(filename, section_name, gemini_client)
                    print(f"  │  │  │  └─ 生成結果: {len(image_data) if image_data else 0} bytes")
                except Exception as e:
                    print(f"  │  │  │  └─ ❌ 例外発生: {str(e)}")
                    image_data = None
                
                if image_data:
                    output_file.write_bytes(image_data)
                    images_created += 1
                    print(f"  │  │  └─ ✅ 保存完了")
                else:
                    print(f"  │  │  └─ ⚠️  生成失敗")
        
        print(f"  │  └─ {images_created}枚生成完了")
    
    print("  └─ Phase 4完了")
    
    return {
        "visual_map_file": str(visual_map_file),
        "sections": len(sections),
        "text_files": text_files_created,
        "images_created": images_created,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens
    }

