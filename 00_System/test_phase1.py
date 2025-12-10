#!/usr/bin/env python3
"""
Phase 1テストスクリプト
テーマ & ターゲット → concept_definition.md 自動生成をテスト
"""

import sys
from pathlib import Path

# モジュールパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from modules import phase1_research

def main():
    print("=" * 60)
    print("🧪 Phase 1テスト: コンセプト定義")
    print("=" * 60)
    
    # プロジェクトディレクトリ
    project_dir = Path(__file__).parent.parent / "03_Projects" / "20241205_Threads_Monetization"
    
    if not project_dir.exists():
        print(f"❌ プロジェクトが見つかりません: {project_dir}")
        return
    
    print(f"\n📁 プロジェクト: {project_dir.name}")
    print()
    
    # Phase 1実行
    print("[Phase 1] リサーチ & コンセプト定義")
    print("  ⚠️  Claude APIを使用します")
    print()
    
    result = phase1_research.run(
        project_dir,
        theme="Threadsで月5万円稼ぐ方法",
        target="副業を始めたい30代会社員"
    )
    
    if result:
        print("\n" + "=" * 60)
        print("✅ Phase 1完了！")
        print("=" * 60)
        print(f"\n💰 APIコスト:")
        print(f"  Claude入力: {result['input_tokens']:,}トークン")
        print(f"  Claude出力: {result['output_tokens']:,}トークン")
        claude_cost = (result['input_tokens'] / 1_000_000 * 3) + (result['output_tokens'] / 1_000_000 * 15)
        print(f"  推定コスト: ${claude_cost:.2f} ≈ ¥{int(claude_cost * 156)}")
        print(f"\n📁 生成ファイル:")
        print(f"  ✅ {result['concept_file']}")
        print("\n🎉 テスト成功！")
        print("=" * 60)
        
        # concept_definition.mdの内容を表示
        print("\n📄 生成されたconcept_definition.mdの内容:")
        print("-" * 60)
        concept_path = Path(result['concept_file'])
        if concept_path.exists():
            content = concept_path.read_text(encoding="utf-8")
            print(content)
        print("-" * 60)
    else:
        print("\n❌ Phase 1失敗")

if __name__ == "__main__":
    main()

