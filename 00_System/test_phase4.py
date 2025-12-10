#!/usr/bin/env python3
"""
Phase 4テストスクリプト
structure_plan.md → visual_map.md 自動生成をテスト
"""

import sys
from pathlib import Path

# モジュールパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from modules import phase4_writing

def main():
    print("=" * 60)
    print("🧪 Phase 4テスト: visual_map.md 自動生成")
    print("=" * 60)
    
    # プロジェクトディレクトリ
    project_dir = Path(__file__).parent.parent / "03_Projects" / "20241205_Threads_Monetization"
    
    if not project_dir.exists():
        print(f"❌ プロジェクトが見つかりません: {project_dir}")
        return
    
    print(f"\n📁 プロジェクト: {project_dir.name}")
    print()
    
    # Phase 4実行
    print("[Phase 4] 執筆 & 画像生成")
    print("  ⚠️  Claude API & Gemini APIを使用します")
    print()
    
    result = phase4_writing.run(
        project_dir,
        enable_text_generation=True,
        enable_image_generation=True,
        prefer_gemini_for_text=True  # Claude残高不足時はGeminiでテキスト生成
    )
    
    if result:
        print("\n" + "=" * 60)
        print("✅ Phase 4完了！")
        print("=" * 60)
        print(f"\n📊 結果:")
        print(f"  セクション数: {result['sections']}")
        print(f"  テキストファイル: {result['text_files']}ファイル")
        print(f"  生成画像: {result['images_created']}枚")
        print(f"\n💰 APIコスト:")
        print(f"  Claude入力: {result['total_input_tokens']:,}トークン")
        print(f"  Claude出力: {result['total_output_tokens']:,}トークン")
        claude_cost = (result['total_input_tokens'] / 1_000_000 * 3) + (result['total_output_tokens'] / 1_000_000 * 15)
        print(f"  推定コスト: ${claude_cost:.2f} ≈ ¥{int(claude_cost * 156)}")
        print(f"\n📁 生成ファイル:")
        print(f"  ✅ {result['visual_map_file']}")
        print("\n🎉 テスト成功！")
        print("=" * 60)
        
        # visual_map.mdの内容を表示
        print("\n📄 生成されたvisual_map.mdの内容:")
        print("-" * 60)
        visual_map_path = Path(result['visual_map_file'])
        if visual_map_path.exists():
            content = visual_map_path.read_text(encoding="utf-8")
            # 最初の50行を表示
            lines = content.split("\n")
            for i, line in enumerate(lines[:50], 1):
                print(line)
            if len(lines) > 50:
                print(f"\n... (残り{len(lines) - 50}行)")
        print("-" * 60)
    else:
        print("\n❌ Phase 4失敗")

if __name__ == "__main__":
    main()

