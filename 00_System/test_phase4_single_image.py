#!/usr/bin/env python3
"""
Phase 4画像生成テスト（1枚のみ）
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.phase4_writing import load_api_keys, generate_image_with_gemini
from google import genai

def main():
    print("=" * 60)
    print("🧪 Phase 4画像生成テスト（1枚のみ）")
    print("=" * 60)
    
    # APIキー読み込み
    print("\n1. APIキー読み込み...")
    claude_key, gemini_key = load_api_keys()
    
    if not gemini_key:
        print("  ❌ Gemini APIキーが見つかりません")
        return
    
    print("  ✅ Gemini APIキー: OK")
    
    # Geminiクライアント初期化
    print("\n2. Geminiクライアント初期化...")
    gemini_client = genai.Client(api_key=gemini_key)
    print("  ✅ クライアント初期化完了")
    
    # テスト画像生成
    print("\n3. テスト画像生成...")
    test_filename = "ill_threads_advantage.png"
    test_section = "なぜ今Threadsなのか？月5万円稼げる3つの理由"
    
    print(f"  ファイル名: {test_filename}")
    print(f"  セクション: {test_section}")
    
    image_data = generate_image_with_gemini(test_filename, test_section, gemini_client)
    
    if image_data:
        print(f"\n  ✅ 画像生成成功！")
        print(f"  データサイズ: {len(image_data)} bytes")
        
        # 保存
        output_file = Path("/tmp/test_phase4_image.png")
        output_file.write_bytes(image_data)
        print(f"  💾 保存完了: {output_file}")
    else:
        print(f"\n  ❌ 画像生成失敗")

if __name__ == "__main__":
    main()

