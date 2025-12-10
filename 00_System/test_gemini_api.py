#!/usr/bin/env python3
"""
Gemini API接続テスト
"""

import os
from pathlib import Path
from google import genai

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
    print("🧪 Gemini API接続テスト")
    print("=" * 60)
    
    # APIキー読み込み
    print("\n1️⃣ APIキー読み込み中...")
    api_key = load_gemini_key()
    
    if not api_key:
        print("❌ APIキーが見つかりません")
        return
    
    print(f"✅ APIキー: {api_key[:10]}...{api_key[-5:]}")
    
    # クライアント初期化
    print("\n2️⃣ Geminiクライアント初期化中...")
    try:
        client = genai.Client(api_key=api_key)
        print("✅ クライアント初期化成功")
    except Exception as e:
        print(f"❌ クライアント初期化失敗: {e}")
        return
    
    # モデル一覧取得
    print("\n3️⃣ 利用可能なモデルを確認中...")
    try:
        models = client.models.list()
        print("✅ モデル一覧取得成功")
        print("\n📋 利用可能なモデル:")
        for model in models:
            if hasattr(model, 'name'):
                print(f"  - {model.name}")
    except Exception as e:
        print(f"⚠️  モデル一覧取得失敗: {e}")
    
    # 画像生成テスト
    print("\n4️⃣ 画像生成テスト...")
    
    test_models = [
        "gemini-2.0-flash-exp",
        "gemini-exp-1206",
        "imagen-3.0-generate-001",
    ]
    
    for model_name in test_models:
        print(f"\n  テスト中: {model_name}")
        try:
            prompt = """Create a professional marketing banner image.
Requirements:
- 16:9 landscape aspect ratio
- Modern, clean design
- Text: "Threads収益化"
- High contrast colors

IMPORTANT: Output in 16:9 landscape format."""
            
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            
            # レスポンス構造を確認
            print(f"    ✅ APIコール成功")
            print(f"    レスポンスタイプ: {type(response)}")
            
            if hasattr(response, 'candidates'):
                print(f"    candidates数: {len(response.candidates) if response.candidates else 0}")
                
                if response.candidates:
                    for i, candidate in enumerate(response.candidates):
                        print(f"    candidate[{i}]: {type(candidate)}")
                        
                        if hasattr(candidate, 'content'):
                            print(f"      content: {type(candidate.content)}")
                            
                            if hasattr(candidate.content, 'parts'):
                                print(f"      parts数: {len(candidate.content.parts) if candidate.content.parts else 0}")
                                
                                if candidate.content.parts:
                                    for j, part in enumerate(candidate.content.parts):
                                        print(f"        part[{j}]: {type(part)}")
                                        
                                        if hasattr(part, 'inline_data'):
                                            print(f"          inline_data: {type(part.inline_data)}")
                                            
                                            if part.inline_data:
                                                data_size = len(part.inline_data.data) if hasattr(part.inline_data, 'data') else 0
                                                print(f"          🎉 画像データ取得成功！ ({data_size} bytes)")
                                                
                                                # 保存テスト
                                                test_file = Path(f"/tmp/test_{model_name.replace('/', '_')}.png")
                                                test_file.write_bytes(part.inline_data.data)
                                                print(f"          💾 保存: {test_file}")
                                                print(f"          ✅ このモデルは画像生成に使えます！")
                                                return
                                        
                                        if hasattr(part, 'text'):
                                            print(f"          text: {part.text[:100]}...")
            
            print(f"    ⚠️  画像データが見つかりませんでした")
            
        except Exception as e:
            print(f"    ❌ エラー: {str(e)[:200]}")
    
    print("\n" + "=" * 60)
    print("テスト完了")
    print("=" * 60)

if __name__ == "__main__":
    main()

