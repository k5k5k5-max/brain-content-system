#!/usr/bin/env python3
"""
Phase 4-5テストスクリプト
既存のPhase1-3の成果物を使ってPhase4-5のみ実行
"""

import sys
from pathlib import Path

# モジュールパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from modules import phase4_writing, phase5_integration

def main():
    print("=" * 60)
    print("🧪 Phase 4-5テスト: 執筆・画像生成・統合")
    print("=" * 60)
    
    # プロジェクトディレクトリ
    project_dir = Path("/Users/keigo/001_cursor/Brain_Content_System_Ver2/03_Projects/20251208_Threadsで月5万円稼ぐ方法")
    
    if not project_dir.exists():
        print(f"❌ プロジェクトが見つかりません: {project_dir}")
        return
    
    print(f"\n📁 プロジェクト: {project_dir.name}")
    print()
    
    # Phase 4実行
    print("[Phase 4] 執筆 & 画像生成")
    print("  ⚠️  Claude API & Gemini APIを使用します")
    print()
    
    config = {
        'enable_text_generation': True,
        'enable_image_generation': True
    }
    
    result4 = phase4_writing.run(project_dir, **config)
    
    if not result4:
        print("\n❌ Phase 4失敗")
        return
    
    # Phase 5実行
    print("\n[Phase 5] 統合 & パッケージング")
    result5 = phase5_integration.run(project_dir)
    
    if not result5:
        print("\n❌ Phase 5失敗")
        return
    
    # 結果表示
    print("\n" + "=" * 60)
    print("✅ Phase 4-5完了！")
    print("=" * 60)
    
    print(f"\n📊 Phase 4結果:")
    print(f"  テキストファイル: {result4.get('text_count', 0)}個")
    print(f"  画像: {result4.get('image_count', 0)}枚")
    
    print(f"\n📊 Phase 5結果:")
    print(f"  総文字数: {result5.get('total_chars', 0):,}文字")
    print(f"  画像数: {result5.get('image_count', 0)}枚")
    
    print(f"\n💰 APIコスト:")
    input_tokens = result4.get('total_input_tokens', 0)
    output_tokens = result4.get('total_output_tokens', 0)
    claude_cost = (input_tokens / 1_000_000 * 3) + (output_tokens / 1_000_000 * 15)
    print(f"  Claude入力: {input_tokens:,}トークン")
    print(f"  Claude出力: {output_tokens:,}トークン")
    print(f"  推定コスト: ${claude_cost:.2f} ≈ ¥{int(claude_cost * 156)}")
    
    print(f"\n📁 成果物:")
    print(f"  ✅ {result5.get('final_md', '')}")
    print(f"  ✅ {result5.get('final_html', '')}")
    print(f"  ✅ {result5.get('images_zip', '')}")
    
    print("\n🎉 テスト成功！")
    print("=" * 60)

if __name__ == "__main__":
    main()

