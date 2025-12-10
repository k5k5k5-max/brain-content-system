#!/usr/bin/env python3
"""
シンプルな画像埋め込みテスト
structure_plan.mdから直接画像情報を取得
"""

import re
from pathlib import Path

def parse_structure_for_images(structure_file):
    """structure_plan.mdから画像配置情報を直接抽出"""
    if not structure_file.exists():
        return {}
    
    content = structure_file.read_text(encoding="utf-8")
    
    # セクションごとの画像配置マップ
    image_map = {}
    
    current_section = None
    current_position = "後"
    current_images = []
    
    for line in content.split("\n"):
        line_stripped = line.strip()
        
        # セクション見出しを検出（### で始まる行）
        if line_stripped.startswith("### "):
            # 前のセクションを保存
            if current_section and current_images:
                image_map[current_section] = {
                    "position": current_position,
                    "images": current_images.copy()
                }
            
            # 新しいセクション
            section_name = line_stripped[4:].strip()
            if ":" in section_name:
                section_name = section_name.split(":", 1)[1].strip()
            
            current_section = section_name
            current_images = []
            current_position = "後"  # デフォルト
        
        # 配置位置を検出
        elif line_stripped.startswith("- **画像**:") or line_stripped.startswith("- **画像**："):
            pass  # 次の行から画像情報
        
        # 画像ファイル名を検出（  - で始まり .png を含む）
        elif line_stripped.startswith("- ") and ".png" in line_stripped:
            # ファイル名を抽出
            match = re.search(r'([a-zA-Z0-9_]+\.png)', line_stripped)
            if match:
                filename = match.group(1)
                current_images.append(filename)
                
                # 配置位置を抽出
                if "配置位置:" in line_stripped or "配置位置：" in line_stripped:
                    pos_match = re.search(r'配置位置[：:]\s*([前中後])', line_stripped)
                    if pos_match:
                        current_position = pos_match.group(1)
    
    # 最後のセクションを保存
    if current_section and current_images:
        image_map[current_section] = {
            "position": current_position,
            "images": current_images
        }
    
    return image_map

# テスト
project_dir = Path("/Users/keigo/001_cursor/Brain_Content_System_Ver2/03_Projects/20251208_Threadsで月5万円稼ぐ方法")
structure_file = project_dir / "02_Planning" / "structure_plan.md"

print("=" * 60)
print("🧪 シンプル画像埋め込みテスト")
print("=" * 60)

image_map = parse_structure_for_images(structure_file)

print(f"\n📊 結果:")
print(f"  セクション数: {len(image_map)}")
print(f"  総画像数: {sum(len(data['images']) for data in image_map.values())}")

print(f"\n📋 セクション詳細:")
for section_name, data in list(image_map.items())[:5]:
    print(f"  - {section_name}")
    print(f"    位置: {data['position']}")
    print(f"    画像: {', '.join(data['images'])}")

print("\n" + "=" * 60)

