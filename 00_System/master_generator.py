#!/usr/bin/env python3
"""
Brain Content System Ver2.0 - Master Generator
1コマンドでBrain/Tips記事を完成させるメインスクリプト
"""

import argparse
import sys
import time
from pathlib import Path
from datetime import datetime
import json

# モジュールパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from modules import phase1_research, phase2_knowhow, phase3_structure
from modules import phase4_writing, phase5_integration, phase6_drive_upload


def print_header():
    """ヘッダー表示"""
    print("\n🚀 Brain Content System Ver2.0 起動")
    print("━" * 60)


def print_footer(start_time, stats):
    """フッター表示"""
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n━" * 60)
    print("🎉 記事生成完了！")
    print("\n📊 統計情報:")
    print(f"  総文字数: {stats['total_chars']:,}文字")
    print(f"  画像数: {stats['image_count']}枚")
    print(f"  所要時間: {minutes}分{seconds}秒")
    print(f"\n  Claude API使用量:")
    print(f"    入力: {stats['claude_input_tokens']:,}トークン (${stats['claude_input_cost']:.3f})")
    print(f"    出力: {stats['claude_output_tokens']:,}トークン (${stats['claude_output_cost']:.3f})")
    print(f"\n  Gemini API使用量:")
    print(f"    画像生成: {stats['image_count']}枚 (無料枠内)")
    print(f"\n💰 今回のコスト: ${stats['total_cost']:.3f} ≈ ¥{int(stats['total_cost'] * 156)}")
    print(f"\n📁 成果物:")
    print(f"  ✅ {stats['output_md']}")
    print(f"  ✅ {stats['output_html']}")
    print(f"  ✅ {stats['output_zip']}")
    
    if stats.get('drive_url'):
        print(f"\n📂 Googleドライブ:")
        print(f"  🔗 {stats['drive_url']}")
    
    print(f"\n🚀 次のステップ:")
    if stats.get('drive_url'):
        print("  1. 外注さんにGoogleドライブのリンクを共有")
        print("  2. Brain/Tipsにアップロード依頼")
    else:
        print("  1. final_article.htmlをBrainにアップロード")
        print("  2. images.zipを解凍して画像を配置")
    print("  3. 価格設定（推奨: 4,980円 → 100円 24時間限定）")
    print("  4. LINE登録リンクを設定")
    print("━" * 60)
    print()


def create_project_directory(theme):
    """プロジェクトディレクトリを作成"""
    # プロジェクト名を生成（日付 + テーマの略称）
    date_str = datetime.now().strftime("%Y%m%d")
    theme_short = theme.replace(" ", "_")[:20]
    project_name = f"{date_str}_{theme_short}"
    
    # ベースディレクトリ
    base_dir = Path(__file__).parent.parent / "03_Projects" / project_name
    
    # サブディレクトリを作成
    (base_dir / "01_Research").mkdir(parents=True, exist_ok=True)
    (base_dir / "02_Planning").mkdir(parents=True, exist_ok=True)
    (base_dir / "03_Content_Draft").mkdir(parents=True, exist_ok=True)
    (base_dir / "04_Images" / "illustrations").mkdir(parents=True, exist_ok=True)
    (base_dir / "04_Images" / "banners").mkdir(parents=True, exist_ok=True)
    (base_dir / "04_Images" / "text_banners").mkdir(parents=True, exist_ok=True)
    (base_dir / "04_Images" / "bonus_thumbnails").mkdir(parents=True, exist_ok=True)
    (base_dir / "05_Final").mkdir(parents=True, exist_ok=True)
    
    return base_dir


def run_phase1(project_dir, theme, target, config):
    """Phase 1: リサーチ & コンセプト定義"""
    print("\n[Phase 1] リサーチ & コンセプト定義")
    result = phase1_research.run(project_dir, theme, target)
    return result if result else {}


def run_phase2(project_dir, phase1_output, config):
    """Phase 2: ノウハウ抽出"""
    print("\n[Phase 2] ノウハウ抽出")
    keyword = config.get('youtube_keyword', 'Threads 稼ぐ方法')
    max_videos = config.get('max_youtube_videos', 3)
    result = phase2_knowhow.run(project_dir, keyword=keyword, max_videos=max_videos)
    return result if result else {}


def run_phase3(project_dir, phase2_output, config):
    """Phase 3: 構成設計 & ビジュアル計画"""
    print("\n[Phase 3] 構成設計 & ビジュアル計画")
    result = phase3_structure.run(project_dir)
    return result if result else {}


def run_phase4(project_dir, phase3_output, config):
    """Phase 4: 執筆 & 画像生成"""
    print("\n[Phase 4] 執筆 & 画像生成")
    enable_text = config.get('enable_text_generation', True)
    enable_image = config.get('enable_image_generation', True)
    prefer_gemini_for_text = config.get('prefer_gemini_for_text', False)
    result = phase4_writing.run(
        project_dir,
        enable_text_generation=enable_text,
        enable_image_generation=enable_image,
        prefer_gemini_for_text=prefer_gemini_for_text
    )
    return result if result else {}


def run_phase5(project_dir, phase4_output, config):
    """Phase 5: 統合 & パッケージング"""
    print("\n[Phase 5] 統合 & パッケージング")
    result = phase5_integration.run(project_dir)
    return result if result else {}


def run_phase6(project_dir, phase5_output, config, theme):
    """Phase 6: Googleドライブアップロード"""
    # Phase 6が無効の場合はスキップ
    if not config.get('enable_drive_upload', False):
        return {}
    
    print("\n[Phase 6] Googleドライブアップロード")
    result = phase6_drive_upload.run(project_dir, theme, config)
    return result if result else {}


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description="Brain Content System Ver2.0")
    parser.add_argument("--theme", required=True, help="記事のテーマ")
    parser.add_argument("--target", default="副業を始めたい30代会社員", help="ターゲットペルソナ")
    parser.add_argument("--config", help="設定ファイルパス（JSON）")
    
    args = parser.parse_args()
    
    # 開始時刻
    start_time = time.time()
    
    # ヘッダー表示
    print_header()
    
    # 設定読み込み
    config = {}
    if args.config and Path(args.config).exists():
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    
    # 設定確認表示
    print(f"\n📋 設定確認:")
    print(f"  テーマ: {args.theme}")
    print(f"  ターゲット: {args.target}")
    
    # プロジェクトディレクトリ作成
    project_dir = create_project_directory(args.theme)
    print(f"  プロジェクト: {project_dir.name}")
    print("\n" + "━" * 60)
    
    # Phase 1
    phase1_output = run_phase1(project_dir, args.theme, args.target, config)
    
    # Phase 2
    phase2_output = run_phase2(project_dir, phase1_output, config)
    
    # Phase 3
    phase3_output = run_phase3(project_dir, phase2_output, config)
    
    # Phase 4
    phase4_output = run_phase4(project_dir, phase3_output, config)
    
    # Phase 5
    phase5_output = run_phase5(project_dir, phase4_output, config)
    
    # Phase 6
    phase6_output = run_phase6(project_dir, phase5_output, config, args.theme)
    
    # 統計情報
    total_input_tokens = (
        phase1_output.get('input_tokens', 0) +
        phase2_output.get('input_tokens', 0) +
        phase3_output.get('input_tokens', 0) +
        phase4_output.get('total_input_tokens', 0)
    )
    total_output_tokens = (
        phase1_output.get('output_tokens', 0) +
        phase2_output.get('output_tokens', 0) +
        phase3_output.get('output_tokens', 0) +
        phase4_output.get('total_output_tokens', 0)
    )
    
    input_cost = total_input_tokens / 1_000_000 * 3
    output_cost = total_output_tokens / 1_000_000 * 15
    total_cost = input_cost + output_cost
    
    stats = {
        "total_chars": phase5_output.get("total_chars", 0),
        "image_count": phase5_output.get("image_count", 0),
        "claude_input_tokens": total_input_tokens,
        "claude_output_tokens": total_output_tokens,
        "claude_input_cost": input_cost,
        "claude_output_cost": output_cost,
        "total_cost": total_cost,
        "output_md": phase5_output.get("final_md", ""),
        "output_html": phase5_output.get("final_html", ""),
        "output_zip": phase5_output.get("images_zip", ""),
        "drive_url": phase6_output.get("folder_url", "") if phase6_output else ""
    }
    
    # フッター表示
    print_footer(start_time, stats)
    
    # 結果をJSONファイルに保存（batch_runner用）
    result_file = project_dir / "result.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({
            "success": True,
            "theme": args.theme,
            "project_dir": str(project_dir),
            "drive_url": stats.get("drive_url", ""),
            "total_chars": stats["total_chars"],
            "image_count": stats["image_count"],
            "total_cost": stats["total_cost"]
        }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

