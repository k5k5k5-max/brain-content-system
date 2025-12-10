#!/usr/bin/env python3
"""
Phase 5統合処理テストスクリプト
"""

import sys
from pathlib import Path

# モジュールパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from modules import phase5_integration

def main():
    print("=" * 60)
    print("🧪 Phase 5統合処理テスト")
    print("=" * 60)
    
    # プロジェクトディレクトリ
    project_dir = Path(__file__).parent.parent / "03_Projects" / "20241205_Threads_Monetization"
    
    if not project_dir.exists():
        print(f"❌ プロジェクトが見つかりません: {project_dir}")
        return
    
    print(f"\n📁 プロジェクト: {project_dir.name}")
    print()
    
    # Phase 5実行
    print("[Phase 5] 統合 & パッケージング")
    result = phase5_integration.run(project_dir)
    
    if result:
        print("\n" + "=" * 60)
        print("✅ 統合処理完了！")
        print("=" * 60)
        print(f"\n📊 結果:")
        print(f"  総文字数: {result['total_chars']:,}文字")
        print(f"  画像数: {result['image_count']}枚")
        print(f"\n📁 成果物:")
        print(f"  ✅ {result['final_md']}")
        print(f"  ✅ {result['final_html']}")
        print(f"  ✅ {result['images_zip']}")
        print("\n🎉 テスト成功！")
        print("=" * 60)
    else:
        print("\n❌ 統合処理失敗")

if __name__ == "__main__":
    main()

