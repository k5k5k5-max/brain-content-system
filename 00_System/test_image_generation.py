#!/usr/bin/env python3
"""
画像生成特化テスト
"""

import os
from pathlib import Path
from google import genai
from google.genai import types

def load_gemini_key():
    """Gemini APIキーを読み込む"""
    gemini_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    
    if not gemini_key:
        env_path = Path("/Users/keigo/001_cursor/.env")
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]:
                            gemini_key = value.strip()
                            break
    
    return gemini_key

def main():
    print("=" * 60)
    print("🧪 画像生成特化テスト")
    print("=" * 60)
    
    api_key = load_gemini_key()
    if not api_key:
        print("❌ APIキーが見つかりません")
        return
    
    client = genai.Client(api_key=api_key)
    
    # テストするモデルとプロンプト
    test_cases = [
        {
            "model": "gemini-2.0-flash-exp-image-generation",
            "prompt": "Threads収益化の16:9マーケティングバナー画像を生成してください。モダンでクリーンなデザイン。"
        },
        {
            "model": "gemini-3-pro-image-preview",
            "prompt": "Create a 16:9 landscape marketing banner for Threads monetization. Modern, clean design with Japanese text 'Threads収益化'."
        },
        {
            "model": "imagen-4.0-generate-001",
            "prompt": "Professional marketing banner, 16:9 landscape, text 'Threads収益化', modern design"
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"テスト {i}: {test['model']}")
        print(f"{'='*60}")
        
        try:
            print(f"📝 プロンプト: {test['prompt'][:50]}...")
            
            response = client.models.generate_content(
                model=test['model'],
                contents=test['prompt']
            )
            
            print(f"✅ APIコール成功")
            
            # レスポンス詳細を確認
            saved = False
            
            if hasattr(response, 'candidates') and response.candidates:
                for cand_idx, candidate in enumerate(response.candidates):
                    if hasattr(candidate, 'content') and candidate.content:
                        if hasattr(candidate.content, 'parts') and candidate.content.parts:
                            for part_idx, part in enumerate(candidate.content.parts):
                                # inline_dataをチェック
                                if hasattr(part, 'inline_data') and part.inline_data:
                                    if hasattr(part.inline_data, 'data'):
                                        data = part.inline_data.data
                                        print(f"  🎉 画像データ発見！ ({len(data)} bytes)")
                                        
                                        # 保存
                                        output_file = Path(f"/tmp/test_{test['model'].replace('/', '_')}_{i}.png")
                                        output_file.write_bytes(data)
                                        print(f"  💾 保存: {output_file}")
                                        saved = True
                                        break
                                
                                # textをチェック
                                if hasattr(part, 'text') and part.text:
                                    print(f"  📄 テキストレスポンス: {part.text[:100]}...")
                    
                    if saved:
                        break
            
            if not saved:
                print(f"  ⚠️  画像データが見つかりませんでした")
                
                # レスポンス全体を表示
                print(f"  🔍 レスポンス詳細:")
                print(f"    type: {type(response)}")
                if hasattr(response, '__dict__'):
                    for key, value in response.__dict__.items():
                        print(f"    {key}: {type(value)}")
        
        except Exception as e:
            print(f"❌ エラー: {str(e)[:300]}")
    
    print("\n" + "=" * 60)
    print("テスト完了")
    print("=" * 60)

if __name__ == "__main__":
    main()

