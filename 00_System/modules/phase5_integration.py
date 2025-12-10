#!/usr/bin/env python3
"""
Phase 5: 統合 & パッケージング
テキスト + 画像を1つの完成記事にまとめる
"""

from pathlib import Path
import zipfile
import json
import re
from datetime import datetime


def collect_text_files(draft_dir):
    """テキストファイルを収集して順番にソート"""
    files = list(draft_dir.glob("*.md"))
    # ファイル名でソート（00_, 01_, 02_...）
    files.sort()
    return files


def collect_images(images_dir):
    """画像ファイルを収集"""
    images = {
        "illustrations": list((images_dir / "illustrations").glob("*.png")),
        "banners": list((images_dir / "banners").glob("*.png")),
        "text_banners": list((images_dir / "text_banners").glob("*.png")),
        "bonus_thumbnails": list((images_dir / "bonus_thumbnails").glob("*.png")),
    }
    
    # 全画像リスト
    all_images = []
    for category, img_list in images.items():
        all_images.extend([(category, img) for img in img_list])
    
    return images, all_images


def integrate_texts(text_files):
    """テキストファイルを統合"""
    combined = []
    
    for i, text_file in enumerate(text_files):
        content = text_file.read_text(encoding="utf-8")
        
        # ファイル名からセクション名を推測
        filename = text_file.stem
        if "Free_Part" in filename:
            section_title = "📖 無料パート"
        elif "Paid_Part" in filename:
            if "Intro" in filename or "Step1" in filename:
                section_title = "💎 有料パート - イントロダクション & STEP 1"
            elif "Step2" in filename:
                section_title = "💎 有料パート - STEP 2"
            elif "Step3" in filename:
                section_title = "💎 有料パート - STEP 3"
            elif "Step4" in filename:
                section_title = "💎 有料パート - STEP 4"
            elif "Step5" in filename:
                section_title = "💎 有料パート - STEP 5"
            elif "Conclusion" in filename:
                section_title = "💎 有料パート - 結論"
            else:
                section_title = "💎 有料パート"
        else:
            section_title = f"セクション {i+1}"
        
        # セクションヘッダーを追加
        combined.append(f"\n\n{'='*60}\n{section_title}\n{'='*60}\n\n")
        combined.append(content)
    
    return "".join(combined)


def parse_visual_map(visual_map_file):
    """visual_map.md を解析して画像配置情報を取得"""
    if not visual_map_file.exists():
        return {}
    
    content = visual_map_file.read_text(encoding="utf-8")
    
    # 画像配置マップ
    image_map = {}
    
    current_section = None
    current_position = "後"  # デフォルト
    
    for line in content.split("\n"):
        line = line.strip()
        
        # セクション見出しを検出（### で始まる行）
        if line.startswith("### "):
            # セクション名と配置位置を抽出
            section_line = line[4:]  # "### " を除去
            
            # 配置位置を抽出（例: "セクション名（前）" → "セクション名", "前"）
            if "（" in section_line and "）" in section_line:
                section_name = section_line[:section_line.rfind("（")].strip()
                position = section_line[section_line.rfind("（")+1:section_line.rfind("）")].strip()
            else:
                section_name = section_line.strip()
                position = "後"
            
            current_section = section_name
            current_position = position
            image_map[current_section] = {
                "position": current_position,
                "images": []
            }
        
        # 画像ファイルを検出（- で始まる行）
        elif line.startswith("- ") and current_section:
            image_file = line[2:].strip()
            image_map[current_section]["images"].append(image_file)
    
    return image_map


def parse_structure_for_images(structure_file):
    """structure_plan.mdから画像配置情報を直接抽出"""
    import re
    
    if not structure_file.exists():
        return {}
    
    content = structure_file.read_text(encoding="utf-8")
    image_map = {}
    current_section = None
    current_position = "後"
    current_images = []
    
    for line in content.split("\n"):
        line_stripped = line.strip()
        
        if line_stripped.startswith("### "):
            if current_section and current_images:
                image_map[current_section] = {
                    "position": current_position,
                    "images": current_images.copy()
                }
            
            section_name = line_stripped[4:].strip()
            if ":" in section_name:
                section_name = section_name.split(":", 1)[1].strip()
            
            current_section = section_name
            current_images = []
            current_position = "後"
        
        elif line_stripped.startswith("- ") and ".png" in line_stripped:
            match = re.search(r'([a-zA-Z0-9_]+\.png)', line_stripped)
            if match:
                filename = match.group(1)
                current_images.append(filename)
                
                if "配置位置:" in line_stripped or "配置位置：" in line_stripped:
                    pos_match = re.search(r'配置位置[：:]\s*([前中後])', line_stripped)
                    if pos_match:
                        current_position = pos_match.group(1)
    
    if current_section and current_images:
        image_map[current_section] = {
            "position": current_position,
            "images": current_images
        }
    
    return image_map


def embed_images_markdown(text, images_by_category, images_dir, visual_map_file):
    """Markdownに画像を埋め込む（structure_plan.md に基づいて配置）"""
    # structure_plan.mdから直接画像情報を取得
    project_dir = visual_map_file.parent.parent
    structure_file = project_dir / "02_Planning" / "structure_plan.md"
    
    image_map = parse_structure_for_images(structure_file)
    
    if not image_map:
        print("  ⚠️  structure_plan.md が見つからないため、デフォルト配置を使用")
        return embed_images_markdown_default(text, images_by_category, images_dir)
    
    # セクションごとに画像を配置
    result = text
    
    print(f"  🔍 DEBUG: image_map内のセクション数={len(image_map)}")
    
    images_placed = 0
    
    for section_name, section_data in image_map.items():
        position = section_data["position"]
        images_list = section_data["images"]
        
        if not images_list:
            continue
        
        # セクション見出しを検索
        # 複数の見出しレベルに対応（##, ###）
        section_patterns = [
            f"## {section_name}",
            f"### {section_name}",
        ]
        
        section_found = False
        for pattern in section_patterns:
            if pattern in result:
                section_found = True
                print(f"    ✅ 見出し発見: {pattern}")
                
                # 配置位置を決定
                if position == "前":
                    # 見出しの直後に挿入
                    insert_pos = result.find(pattern) + len(pattern)
                    # 次の改行の後に挿入
                    next_newline = result.find("\n", insert_pos)
                    if next_newline != -1:
                        insert_pos = next_newline + 1
                
                elif position == "後":
                    # セクションの終わり（次のセクション見出しの前）に挿入
                    section_start = result.find(pattern)
                    
                    # 次のセクション見出しを探す
                    next_section_patterns = ["\n## ", "\n### ", "\n===="]
                    next_section_pos = len(result)
                    
                    for next_pattern in next_section_patterns:
                        pos = result.find(next_pattern, section_start + len(pattern))
                        if pos != -1 and pos < next_section_pos:
                            next_section_pos = pos
                    
                    insert_pos = next_section_pos
                
                else:  # "中" または デフォルト
                    # セクションの中間に挿入（後と同じ処理）
                    section_start = result.find(pattern)
                    next_section_patterns = ["\n## ", "\n### ", "\n===="]
                    next_section_pos = len(result)
                    
                    for next_pattern in next_section_patterns:
                        pos = result.find(next_pattern, section_start + len(pattern))
                        if pos != -1 and pos < next_section_pos:
                            next_section_pos = pos
                    
                    insert_pos = next_section_pos
                
                # 画像を挿入
                image_inserts = "\n\n"
                for image_file in images_list:
                    # 画像カテゴリを推測
                    if "ill_" in image_file:
                        category = "illustrations"
                    elif "banner_" in image_file:
                        category = "banners"
                    elif "text_banner_" in image_file:
                        category = "text_banners"
                    elif "bonus_" in image_file:
                        category = "bonus_thumbnails"
                    else:
                        category = "illustrations"
                    
                    rel_path = f"../04_Images/{category}/{image_file}"
                    image_name = image_file.replace(".png", "").replace("_", " ")
                    image_inserts += f"![{image_name}]({rel_path})\n\n"
                
                # テキストに挿入
                result = result[:insert_pos] + image_inserts + result[insert_pos:]
                images_placed += len(images_list)
                
                break  # セクションが見つかったらループを抜ける
        
        if not section_found:
            print(f"  ⚠️  セクション「{section_name}」が見つかりませんでした")
    
    print(f"  📊 合計: {images_placed}枚の画像を配置")
    
    return result


def embed_images_markdown_default(text, images_by_category, images_dir):
    """デフォルトの画像埋め込み（visual_map.md がない場合）"""
    result = text
    
    # 無料パートにイラストを挿入
    if "無料パート" in text:
        free_section_end = text.find("有料パート")
        if free_section_end == -1:
            free_section_end = len(text) // 2
        
        # イラストを挿入
        illustrations = images_by_category.get("illustrations", [])
        text_banners = images_by_category.get("text_banners", [])
        
        image_inserts = "\n\n## 📊 ビジュアルで理解する\n\n"
        
        for img in illustrations[:3]:
            rel_path = f"../04_Images/illustrations/{img.name}"
            image_inserts += f"![{img.stem}]({rel_path})\n\n"
        
        for img in text_banners:
            rel_path = f"../04_Images/text_banners/{img.name}"
            image_inserts += f"![{img.stem}]({rel_path})\n\n"
        
        result = result[:free_section_end] + image_inserts + result[free_section_end:]
    
    # ボーナスサムネイルを最後に挿入
    bonus_thumbnails = images_by_category.get("bonus_thumbnails", [])
    if bonus_thumbnails:
        bonus_section = "\n\n## 🎁 購入者限定追加特典\n\n"
        for img in bonus_thumbnails[:3]:
            rel_path = f"../04_Images/bonus_thumbnails/{img.name}"
            bonus_section += f"![{img.stem}]({rel_path})\n\n"
        
        result += bonus_section
    
    return result


def convert_to_html(markdown_text):
    """MarkdownをHTMLに変換（簡易版）"""
    html = markdown_text
    
    # 見出しの変換
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 画像の変換
    html = re.sub(
        r'!\[([^\]]*)\]\(([^\)]+)\)',
        r'<img src="\2" alt="\1" style="max-width:100%; height:auto;" />',
        html
    )
    
    # リストの変換
    html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    
    # 段落の変換
    html = html.replace('\n\n', '</p><p>')
    
    # HTMLテンプレート
    full_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Threadsで月5万円稼ぐ方法</title>
    <style>
        body {{
            font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
            line-height: 1.8;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            font-size: 2em;
        }}
        h2 {{
            color: #34495e;
            border-left: 5px solid #3498db;
            padding-left: 15px;
            margin-top: 40px;
            font-size: 1.5em;
        }}
        h3 {{
            color: #7f8c8d;
            font-size: 1.2em;
        }}
        img {{
            display: block;
            margin: 30px auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        p {{
            color: #555;
            margin: 15px 0;
        }}
        ul {{
            background: white;
            padding: 20px 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        li {{
            margin: 10px 0;
            color: #555;
        }}
        .section-divider {{
            border-top: 2px dashed #ddd;
            margin: 60px 0;
        }}
    </style>
</head>
<body>
<p>{html}</p>
</body>
</html>"""
    
    return full_html


def create_zip(images_dir, output_zip):
    """画像をZIP化"""
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for category in ["illustrations", "banners", "text_banners", "bonus_thumbnails"]:
            category_dir = images_dir / category
            if category_dir.exists():
                for img in category_dir.glob("*.png"):
                    arcname = f"{category}/{img.name}"
                    zipf.write(img, arcname)
    
    return output_zip


def create_metadata(stats, output_file):
    """メタデータJSON作成"""
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "total_chars": stats["total_chars"],
        "image_count": stats["image_count"],
        "sections": stats["sections"],
        "files": stats["files"]
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return output_file


def run(project_dir):
    """Phase 5実行"""
    print("  ├─ テキスト収集中...")
    draft_dir = project_dir / "03_Content_Draft"
    text_files = collect_text_files(draft_dir)
    
    if not text_files:
        print("  ⚠️  テキストファイルが見つかりません")
        return None
    
    print(f"  │  └─ {len(text_files)}ファイル取得")
    
    print("  ├─ 画像収集中...")
    images_dir = project_dir / "04_Images"
    images_by_category, all_images = collect_images(images_dir)
    print(f"  │  └─ {len(all_images)}枚取得")
    
    print("  ├─ テキスト統合中...")
    combined_text = integrate_texts(text_files)
    print(f"  │  └─ {len(combined_text):,}文字")
    
    print("  ├─ 画像埋め込み中...")
    visual_map_file = project_dir / "02_Planning" / "visual_map.md"
    final_markdown = embed_images_markdown(combined_text, images_by_category, images_dir, visual_map_file)
    print(f"  │  └─ {len(all_images)}枚配置")
    
    # 出力ディレクトリ
    final_dir = project_dir / "05_Final"
    final_dir.mkdir(exist_ok=True)
    
    # Markdown保存
    print("  ├─ Markdown保存中...")
    final_md = final_dir / "final_article.md"
    final_md.write_text(final_markdown, encoding="utf-8")
    print(f"  │  └─ {final_md.name}")
    
    # HTML変換
    print("  ├─ HTML変換中...")
    final_html_content = convert_to_html(final_markdown)
    final_html = final_dir / "final_article.html"
    final_html.write_text(final_html_content, encoding="utf-8")
    print(f"  │  └─ {final_html.name}")
    
    # ZIP作成
    print("  ├─ ZIP圧縮中...")
    images_zip = final_dir / "images.zip"
    create_zip(images_dir, images_zip)
    zip_size = images_zip.stat().st_size / (1024 * 1024)  # MB
    print(f"  │  └─ {images_zip.name} ({zip_size:.1f}MB)")
    
    # メタデータ
    print("  └─ メタデータ保存中...")
    stats = {
        "total_chars": len(final_markdown),
        "image_count": len(all_images),
        "sections": len(text_files),
        "files": {
            "markdown": str(final_md),
            "html": str(final_html),
            "zip": str(images_zip)
        }
    }
    metadata_file = final_dir / "metadata.json"
    create_metadata(stats, metadata_file)
    print(f"     └─ {metadata_file.name}")
    
    return {
        "final_md": str(final_md),
        "final_html": str(final_html),
        "images_zip": str(images_zip),
        "total_chars": len(final_markdown),
        "image_count": len(all_images)
    }

