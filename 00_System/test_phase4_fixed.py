#!/usr/bin/env python3
"""
修正版Phase 4テスト
見出しが厳密に守られるかテスト
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules import phase4_writing

def main():
    print("=" * 60)
    print("🧪 修正版Phase 4テスト")
    print("=" * 60)
    
    project_dir = Path("/Users/keigo/001_cursor/Brain_Content_System_Ver2/03_Projects/20251208_Threadsで月5万円稼ぐ方法")
    
    print(f"\n📁 プロジェクト: {project_dir.name}")
    print()
    
    print("[Phase 4] 執筆 & 画像生成（修正版）")
    print("  見出しを厳密に守るように修正しました")
    print()
    
    # 最初の3セクションだけテスト
    result = phase4_writing.run(
        project_dir,
        enable_text_generation=True,
        enable_image_generation=False  # 画像は後で
    )
    
    if result:
        print("\n" + "=" * 60)
        print("✅ Phase 4完了！")
        print("=" * 60)
        print(f"\n📊 結果:")
        print(f"  テキストファイル: {result.get('text_files', 0)}個")
        
        # 生成されたファイルの見出しを確認
        print(f"\n📄 生成されたファイルの見出し確認:")
        draft_dir = project_dir / "03_Content_Draft"
        for md_file in sorted(draft_dir.glob("*.md"))[:5]:
            with open(md_file, 'r', encoding='utf-8') as f:
                first_lines = f.read(200)
                heading = first_lines.split('\n')[0] if first_lines else "見出しなし"
                print(f"  - {md_file.name}")
                print(f"    → {heading}")
        
        print("\n🎉 テスト成功！")
    else:
        print("\n❌ Phase 4失敗")

if __name__ == "__main__":
    main()

