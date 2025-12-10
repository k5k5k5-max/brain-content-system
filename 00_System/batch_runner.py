#!/usr/bin/env python3
"""
Daily batch runner for Brain Content System.

- Reads a theme list (CSV/TSV/line-delimited) and runs master_generator.py per theme.
- Forces prefer_gemini_for_text=True so Claude残高ゼロでも動作。
- Sends LINE Notify if LINE_NOTIFY_TOKEN is set (start / each item / summary).

Usage example:
  python3 batch_runner.py \
    --theme-file /Users/keigo/001_cursor/Brain_Content_System_Ver2/theme_list.txt \
    --config /Users/keigo/001_cursor/Brain_Content_System_Ver2/00_System/test_config.json \
    --target "副業初心者の20代会社員" \
    --concurrency 1
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).parent
PROJECT_ROOT = ROOT_DIR.parent
MASTER = ROOT_DIR / "master_generator.py"


def send_line_notify(token: str, message: str) -> None:
    """Send LINE Notify message if token is provided."""
    if not token:
        return
    try:
        import requests  # type: ignore
    except Exception:
        print("⚠️  requests が見つかりません。LINE通知をスキップします。")
        return
    try:
        resp = requests.post(
            "https://notify-api.line.me/api/notify",
            headers={"Authorization": f"Bearer {token}"},
            data={"message": message},
            timeout=10,
        )
        if resp.status_code != 200:
            print(f"⚠️  LINE通知失敗: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"⚠️  LINE通知中に例外: {e}")


def load_theme_list(path: Path) -> List[str]:
    """Load themes from CSV/TSV or plain text."""
    if not path.exists():
        raise FileNotFoundError(f"テーマファイルが見つかりません: {path}")
    text = path.read_text(encoding="utf-8")
    # Try CSV first (comma/tsv)
    themes: List[str] = []
    try:
        dialect = csv.Sniffer().sniff(text.splitlines()[0])
        reader = csv.reader(text.splitlines(), dialect)
        for row in reader:
            for cell in row:
                t = cell.strip()
                if t:
                    themes.append(t)
        if themes:
            return themes
    except Exception:
        pass
    # fallback: line-delimited
    for line in text.splitlines():
        t = line.strip()
        if t:
            themes.append(t)
    return themes


def merge_config(base_config: Path, prefer_gemini_for_text: bool = True) -> Path:
    """Load config JSON, force prefer_gemini_for_text, and write temp config."""
    data = {}
    if base_config.exists():
        data = json.loads(base_config.read_text(encoding="utf-8"))
    data.setdefault("prefer_gemini_for_text", prefer_gemini_for_text)
    tmp = Path("/tmp/brain_batch_config.json")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return tmp


def run_one(theme: str, target: str, config_path: Path, log_dir: Path) -> dict:
    """
    Run master_generator for a single theme.
    
    Returns:
        dict: {
            "success": bool,
            "theme": str,
            "drive_url": str,
            "total_chars": int,
            "image_count": int
        }
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{theme[:24].replace(' ', '_')}.log"
    cmd = [
        sys.executable,
        str(MASTER),
        "--theme",
        theme,
        "--target",
        target,
        "--config",
        str(config_path),
    ]
    print(f"▶️  start: {theme}")
    with log_file.open("w", encoding="utf-8") as f:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        f.write(proc.stdout)
    ok = proc.returncode == 0
    print(f"✅ success: {theme}" if ok else f"❌ failed: {theme}")
    
    # 結果ファイルを読み取り
    result = {"success": ok, "theme": theme, "drive_url": "", "total_chars": 0, "image_count": 0}
    if ok:
        # プロジェクトディレクトリを探す
        date_str = datetime.now().strftime("%Y%m%d")
        theme_short = theme.replace(" ", "_")[:20]
        project_name = f"{date_str}_{theme_short}"
        result_file = PROJECT_ROOT / "03_Projects" / project_name / "result.json"
        if result_file.exists():
            try:
                with open(result_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    result.update(data)
            except Exception as e:
                print(f"⚠️  result.json読み取りエラー: {e}")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Batch runner for Brain Content System")
    parser.add_argument("--theme-file", required=True, help="テーマ一覧ファイル（CSV/TSV/行区切り）")
    parser.add_argument("--config", default=str(ROOT_DIR / "test_config.json"), help="設定ファイルパス")
    parser.add_argument("--target", default="副業を始めたい30代会社員", help="ターゲットペルソナ")
    parser.add_argument("--concurrency", type=int, default=1, help="同時実行数（簡易。>1は将来対応予定）")
    parser.add_argument("--prefer-gemini-for-text", action="store_true", default=True, help="テキスト生成をGemini優先にする")
    args = parser.parse_args()

    themes = load_theme_list(Path(args.theme_file))
    if not themes:
        print("⚠️  テーマが0件です")
        sys.exit(1)

    cfg = merge_config(Path(args.config), prefer_gemini_for_text=args.prefer_gemini_for_text)
    line_token = os.environ.get("LINE_NOTIFY_TOKEN", "").strip()

    batch_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = Path("/tmp/brain_batch_logs") / batch_id

    send_line_notify(line_token, f"🟢 Brainバッチ開始: {len(themes)}件 (batch_id={batch_id})")

    success = 0
    fail = 0
    results = []
    for idx, theme in enumerate(themes, 1):
        msg_head = f"[{idx}/{len(themes)}] {theme}"
        send_line_notify(line_token, f"▶️ {msg_head}")
        result = run_one(theme, args.target, cfg, log_dir)
        results.append(result)
        
        if result["success"]:
            success += 1
            # 成功時にドライブURLを含めて通知
            msg = f"✅ {msg_head}\n"
            if result.get("drive_url"):
                msg += f"📂 {result['drive_url']}\n"
            msg += f"📝 {result.get('total_chars', 0):,}文字 | 🖼 {result.get('image_count', 0)}枚"
            send_line_notify(line_token, msg)
        else:
            fail += 1
            send_line_notify(line_token, f"❌ {msg_head}")
        time.sleep(1)  # 軽いウェイト

    # 最終サマリー
    summary_msg = f"🏁 Brainバッチ完了: 成功{success}/失敗{fail}\n\n"
    if success > 0:
        summary_msg += "【完成した記事】\n"
        for r in results:
            if r["success"]:
                summary_msg += f"✅ {r['theme']}\n"
                if r.get("drive_url"):
                    summary_msg += f"   🔗 {r['drive_url']}\n"
    
    send_line_notify(line_token, summary_msg)
    print(f"完了: 成功{success}, 失敗{fail}, ログ: {log_dir}")


if __name__ == "__main__":
    main()


