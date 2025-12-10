#!/usr/bin/env python3
"""
Phase 2テストスクリプト
YouTube → ノウハウ抽出をテスト
"""

import sys
from pathlib import Path

# モジュールパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from modules import phase2_knowhow

def main():
    print("=" * 60)
    print("🧪 Phase 2テスト: ノウハウ抽出")
    print("=" * 60)
    
    # プロジェクトディレクトリ
    project_dir = Path(__file__).parent.parent / "03_Projects" / "20241205_Threads_Monetization"
    
    if not project_dir.exists():
        print(f"❌ プロジェクトが見つかりません: {project_dir}")
        return
    
    print(f"\n📁 プロジェクト: {project_dir.name}")
    print()
    
    # Phase 2実行
    print("[Phase 2] ノウハウ抽出")
    print("  ⚠️  YouTube検索 & Claude APIを使用します")
    print()
    
    result = phase2_knowhow.run(
        project_dir, 
        keyword="Threads 稼ぐ方法", 
        max_videos=3
    )
    
    if result:
        print("\n" + "=" * 60)
        print("✅ Phase 2完了！")
        print("=" * 60)
        print(f"\n📊 結果:")
        print(f"  YouTube動画: {result['videos_found']}件検索")
        print(f"  字幕取得: {result['transcripts_retrieved']}件")
        print(f"\n💰 APIコスト:")
        print(f"  Claude入力: {result['input_tokens']:,}トークン")
        print(f"  Claude出力: {result['output_tokens']:,}トークン")
        claude_cost = (result['input_tokens'] / 1_000_000 * 3) + (result['output_tokens'] / 1_000_000 * 15)
        print(f"  推定コスト: ${claude_cost:.2f} ≈ ¥{int(claude_cost * 156)}")
        print(f"\n📁 生成ファイル:")
        print(f"  ✅ {result['knowhow_file']}")
        print("\n🎉 テスト成功！")
        print("=" * 60)
        
        # knowhow_extraction.mdの内容を表示
        print("\n📄 生成されたknowhow_extraction.mdの内容:")
        print("-" * 60)
        knowhow_path = Path(result['knowhow_file'])
        if knowhow_path.exists():
            content = knowhow_path.read_text(encoding="utf-8")
            # 最初の100行を表示
            lines = content.split("\n")
            for i, line in enumerate(lines[:100], 1):
                print(line)
            if len(lines) > 100:
                print(f"\n... (残り{len(lines) - 100}行)")
        print("-" * 60)
    else:
        print("\n❌ Phase 2失敗")

if __name__ == "__main__":
    main()
