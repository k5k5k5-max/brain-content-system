#!/usr/bin/env python3
"""
Phase 5のみ実行: テキストを統合してHTML化
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules import phase5_integration

def main():
    project_dir = Path("/Users/keigo/001_cursor/Brain_Content_System_Ver2/03_Projects/20251208_Threadsで月5万円稼ぐ方法")
    
    print("==========")
    print("Phase 5のみ実行: 統合")
    print("==========\n")
    
    result = phase5_integration.run(project_dir)
    
    if result:
        print(f"\n✅ 成功！")
        print(f"  総文字数: {result.get('total_chars', 0):,}文字")
        print(f"  画像数: {result.get('image_count', 0)}枚")
        print(f"\n📁 成果物:")
        print(f"  {result.get('final_md', '')}")
        print(f"  {result.get('final_html', '')}")
    else:
        print("\n❌ 失敗")

if __name__ == "__main__":
    main()

