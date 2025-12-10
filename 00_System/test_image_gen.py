#!/usr/bin/env python3
"""
画像生成デバッグスクリプト
"""

import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent))

from google import genai

def load_gemini_key():
    """Gemini APIキーを読み込む"""
    gemini_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if gemini_key:
        return gemini_key
    
    env_paths = [
        Path("/Users/keigo/001_cursor/.env"),
        Path("/Users/keigo/001_cursor/文字起こしブースター/mioji_share_v2/.env"),
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]:
                                return value.strip()
            except Exception:
                continue
    
    return None

def test_image_generation():
    """画像生成テスト"""
    print("=" * 60)
    print("🧪 Gemini API 画像生成テスト")
    print("=" * 60)
    
    # APIキー読み込み
    print("\n1. APIキー読み込み...")
    gemini_key = load_gemini_key()
    
    if not gemini_key:
        print("  ❌ Gemini APIキーが見つかりません")
        return
    
    print(f"  ✅ APIキー: {gemini_key[:10]}...{gemini_key[-5:]}")
    
    # クライアント初期化
    print("\n2. Geminiクライアント初期化...")
    try:
        gemini_client = genai.Client(api_key=gemini_key)
        print("  ✅ クライアント初期化成功")
    except Exception as e:
        print(f"  ❌ クライアント初期化失敗: {str(e)}")
        return
    
    # モデル確認
    print("\n3. 利用可能なモデル確認...")
    try:
        models = gemini_client.models.list()
        print("  ✅ モデル一覧取得成功")
        print(f"  利用可能なモデル数: {len(list(models))}")
        
        # 画像生成モデルを探す
        image_models = []
        for model in gemini_client.models.list():
            if 'image' in model.name.lower():
                image_models.append(model.name)
        
        if image_models:
            print(f"  画像生成モデル: {', '.join(image_models)}")
        else:
            print("  ⚠️  画像生成モデルが見つかりません")
    except Exception as e:
        print(f"  ❌ モデル一覧取得失敗: {str(e)}")
        return
    
    # テスト画像生成
    print("\n4. テスト画像生成...")
    prompt = """Create a professional banner image for a digital content article.

Image Type: テキストバナー
Section: Threadsで月5万円稼ぐ方法
Filename: test_banner.png

Requirements:
- 16:9 landscape aspect ratio, 1376x768 resolution
- Modern, clean design
- Japanese text: "Threadsで月5万円稼ぐ"
- High contrast for mobile viewing
- Professional marketing aesthetic

Style:
- Bold typography, high impact design
- Gold and black color scheme

IMPORTANT: Output in 16:9 landscape format, 1376x768 pixels.
"""
    
    try:
        print("  📡 API呼び出し中...")
        response = gemini_client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt
        )
        print("  ✅ API呼び出し成功")
        
        # レスポンス解析
        print("\n5. レスポンス解析...")
        print(f"  レスポンス型: {type(response)}")
        print(f"  hasattr candidates: {hasattr(response, 'candidates')}")
        
        if hasattr(response, 'candidates') and response.candidates:
            print(f"  candidates数: {len(response.candidates)}")
            
            for i, candidate in enumerate(response.candidates):
                print(f"\n  Candidate {i+1}:")
                print(f"    hasattr content: {hasattr(candidate, 'content')}")
                
                if hasattr(candidate, 'content') and candidate.content:
                    print(f"    hasattr parts: {hasattr(candidate.content, 'parts')}")
                    
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        print(f"    parts数: {len(candidate.content.parts)}")
                        
                        for j, part in enumerate(candidate.content.parts):
                            print(f"\n    Part {j+1}:")
                            print(f"      type: {type(part)}")
                            print(f"      hasattr inline_data: {hasattr(part, 'inline_data')}")
                            
                            if hasattr(part, 'inline_data') and part.inline_data:
                                image_data = part.inline_data.data
                                print(f"      ✅ 画像データ取得成功！")
                                print(f"      データサイズ: {len(image_data)} bytes")
                                
                                # テスト保存
                                output_file = Path("/tmp/test_gemini_image.png")
                                output_file.write_bytes(image_data)
                                print(f"      💾 保存完了: {output_file}")
                                return
        
        print("\n  ⚠️  画像データが見つかりませんでした")
        print(f"\n  生レスポンス: {response}")
        
    except Exception as e:
        print(f"  ❌ 画像生成失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image_generation()

