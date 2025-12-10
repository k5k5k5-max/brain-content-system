#!/usr/bin/env python3
"""
Phase 3テストスクリプト
ノウハウ & コンセプト → structure_plan.md 自動生成をテスト
"""

import sys
from pathlib import Path

# モジュールパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from modules import phase3_structure

def main():
    print("=" * 60)
    print("🧪 Phase 3テスト: structure_plan.md 自動生成")
    print("=" * 60)
    
    # プロジェクトディレクトリ
    project_dir = Path(__file__).parent.parent / "03_Projects" / "20241205_Threads_Monetization"
    
    if not project_dir.exists():
        print(f"❌ プロジェクトが見つかりません: {project_dir}")
        return
    
    print(f"\n📁 プロジェクト: {project_dir.name}")
    print()
    
    # Phase 3実行
    print("[Phase 3] 構成設計 & ビジュアル計画")
    print("  ⚠️  Claude APIを使用します")
    print()
    
    result = phase3_structure.run(project_dir)
    
    if result:
        print("\n" + "=" * 60)
        print("✅ Phase 3完了！")
        print("=" * 60)
        print(f"\n📊 結果:")
        print(f"  無料パート: {result['free_sections']}セクション")
        print(f"  有料パート: {result['paid_sections']}セクション")
        print(f"\n💰 APIコスト:")
        print(f"  Claude入力: {result['input_tokens']:,}トークン")
        print(f"  Claude出力: {result['output_tokens']:,}トークン")
        claude_cost = (result['input_tokens'] / 1_000_000 * 3) + (result['output_tokens'] / 1_000_000 * 15)
        print(f"  推定コスト: ${claude_cost:.2f} ≈ ¥{int(claude_cost * 156)}")
        print(f"\n📁 生成ファイル:")
        print(f"  ✅ {result['structure_file']}")
        print("\n🎉 テスト成功！")
        print("=" * 60)
        
        # structure_plan.mdの内容を表示
        print("\n📄 生成されたstructure_plan.mdの内容:")
        print("-" * 60)
        structure_path = Path(result['structure_file'])
        if structure_path.exists():
            content = structure_path.read_text(encoding="utf-8")
            # 最初の80行を表示
            lines = content.split("\n")
            for i, line in enumerate(lines[:80], 1):
                print(line)
            if len(lines) > 80:
                print(f"\n... (残り{len(lines) - 80}行)")
        print("-" * 60)
    else:
        print("\n❌ Phase 3失敗")

if __name__ == "__main__":
    main()

