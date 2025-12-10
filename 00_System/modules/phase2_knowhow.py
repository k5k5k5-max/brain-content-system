#!/usr/bin/env python3
"""
Phase 2: ノウハウ抽出
YouTubeから動画を検索し、字幕からノウハウを抽出
"""

from pathlib import Path
import anthropic
import os
import subprocess
import json
import re
import tempfile

# Gemini API
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def load_claude_api_key():
    """Claude APIキーを読み込む"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        return api_key.strip()
    
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
                            if key == "ANTHROPIC_API_KEY":
                                return value.strip()
            except Exception:
                continue
    
    return None


def load_gemini_api_key():
    """Gemini APIキーを読み込む"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        return api_key.strip()
    
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
                            if key == "GEMINI_API_KEY":
                                return value.strip()
            except Exception:
                continue
    
    return None


def search_youtube_videos(keyword, max_results=5):
    """YouTubeで動画を検索（yt-dlp使用）"""
    try:
        # yt-dlpで検索
        search_query = f"ytsearch{max_results}:{keyword}"
        
        # yt-dlpのパスを探す
        ytdlp_paths = [
            "/Users/keigo/Library/Python/3.12/bin/yt-dlp",
            "/usr/local/bin/yt-dlp",
            "yt-dlp"  # PATHにある場合
        ]
        
        ytdlp_cmd = None
        for path in ytdlp_paths:
            try:
                result_check = subprocess.run([path, "--version"], capture_output=True, timeout=5)
                if result_check.returncode == 0:
                    ytdlp_cmd = path
                    break
            except:
                continue
        
        if not ytdlp_cmd:
            print("    ❌ yt-dlpが見つかりません")
            return []
        
        cmd = [
            ytdlp_cmd,
            "--dump-json",
            "--skip-download",
            "--no-warnings",
            search_query
        ]
        
        # コマンド実行
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"    ❌ 検索エラー: {result.stderr}")
            return []
        
        # 結果を解析
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    video_data = json.loads(line)
                    videos.append({
                        'title': video_data.get('title', ''),
                        'id': video_data.get('id', ''),
                        'link': f"https://www.youtube.com/watch?v={video_data.get('id', '')}",
                        'duration': str(video_data.get('duration', 0)),
                        'views': str(video_data.get('view_count', 'N/A'))
                    })
                except:
                    continue
        
        return videos
    
    except Exception as e:
        print(f"    ❌ 検索エラー: {str(e)}")
        return []


def get_video_transcript(video_id, ytdlp_cmd):
    """動画の字幕を取得（yt-dlp使用）"""
    try:
        # 一時ディレクトリで字幕をダウンロード
        with tempfile.TemporaryDirectory() as tmpdir:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            cmd = [
                ytdlp_cmd,
                "--write-auto-sub",
                "--sub-lang", "ja",
                "--skip-download",
                "--sub-format", "json3",
                "-o", f"{tmpdir}/subtitle",
                "--no-warnings",
                video_url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 字幕ファイルを探す
            subtitle_files = list(Path(tmpdir).glob("*.ja.json3"))
            
            if not subtitle_files:
                return None
            
            # 字幕を読み込んで解析
            subtitle_file = subtitle_files[0]
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                subtitle_data = json.load(f)
            
            # テキストを抽出
            if 'events' in subtitle_data:
                texts = []
                for event in subtitle_data['events']:
                    if 'segs' in event:
                        for seg in event['segs']:
                            if 'utf8' in seg:
                                texts.append(seg['utf8'])
                
                full_text = " ".join(texts)
                return full_text
            
            return None
    
    except Exception as e:
        print(f"    ⚠️  字幕取得失敗: {str(e)[:100]}...")
        return None


def extract_knowhow_with_claude(video_data_list, concept_content, claude_client):
    """Claude APIでノウハウを抽出"""
    # 動画情報をまとめる
    videos_summary = ""
    for i, video in enumerate(video_data_list, 1):
        videos_summary += f"\n\n【動画{i}】\nタイトル: {video['title']}\n再生回数: {video['views']}\n\n字幕:\n{video['transcript'][:3000]}...\n"
    
    prompt = f"""あなたはプロのコンテンツリサーチャーです。以下のYouTube動画の字幕から、実践的なノウハウとテクニックを抽出してください。

【コンセプト】
{concept_content}

【YouTube動画の字幕】
{videos_summary}

【タスク】
以下のフォーマットでノウハウを抽出してください：

# ノウハウ抽出

## 主要ノウハウマトリクス

| 項目 | 動画1 | 動画2 | 動画3 | 採用ノウハウ |
|------|-------|-------|-------|------------|
| 基本戦略 | ... | ... | ... | ... |
| 収益化手法 | ... | ... | ... | ... |
| プロフィール設計 | ... | ... | ... | ... |
| 投稿戦略 | ... | ... | ... | ... |
| AI活用法 | ... | ... | ... | ... |

## 実践テクニック

### 1. [テクニック名]
- 具体的な手順
- ポイント
- 注意点

### 2. [テクニック名]
...

## よくある失敗パターン

1. ...
2. ...

## 重要な注意点

- ...

【抽出ルール】
1. 発信者名や動画タイトルは一切記載しない
2. ノウハウとテクニックのみを抽出
3. 具体的で実践可能な内容に絞る
4. 複数の動画で共通する内容を優先
5. マトリクスは簡潔に（各セル100文字以内）

それでは抽出を開始してください。
"""
    
    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        text = response.content[0].text
        return text, response.usage.input_tokens, response.usage.output_tokens
    
    except Exception as e:
        print(f"    ❌ エラー: {str(e)}")
        return None, 0, 0


def extract_knowhow_with_gemini(video_data_list, concept_content, gemini_client):
    """Gemini APIでノウハウを抽出"""
    # 動画情報をまとめる
    videos_summary = ""
    for i, video in enumerate(video_data_list, 1):
        videos_summary += f"\n\n【動画{i}】\nタイトル: {video['title']}\n再生回数: {video['views']}\n\n字幕:\n{video['transcript'][:3000]}...\n"
    
    prompt = f"""あなたはプロのコンテンツリサーチャーです。以下のYouTube動画の字幕から、実践的なノウハウとテクニックを抽出してください。

【コンセプト】
{concept_content}

【YouTube動画の字幕】
{videos_summary}

【タスク】
以下のフォーマットでノウハウを抽出してください：

# ノウハウ抽出

## 主要ノウハウマトリクス

| 項目 | 動画1 | 動画2 | 動画3 | 採用ノウハウ |
|------|-------|-------|-------|------------|
| 基本戦略 | ... | ... | ... | ... |
| 収益化手法 | ... | ... | ... | ... |
| プロフィール設計 | ... | ... | ... | ... |
| 投稿戦略 | ... | ... | ... | ... |
| AI活用法 | ... | ... | ... | ... |

## 実践テクニック

### 1. [テクニック名]
- 具体的な手順
- ポイント
- 注意点

### 2. [テクニック名]
...

## よくある失敗パターン

1. ...
2. ...

## 重要な注意点

- ...

【抽出ルール】
1. 発信者名や動画タイトルは一切記載しない
2. ノウハウとテクニックのみを抽出
3. 具体的で実践可能な内容に絞る
4. 複数の動画で共通する内容を優先
5. マトリクスは簡潔に（各セル100文字以内）

それでは抽出を開始してください。
"""
    
    try:
        response = gemini_client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=prompt
        )
        text = response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text
        return text, 0, 0  # Geminiのトークン情報は未集計
    
    except Exception as e:
        print(f"    ❌ Geminiエラー: {str(e)}")
        return None, 0, 0


def run(project_dir, keyword="Threads 稼ぐ方法", max_videos=3, prefer_gemini=True):
    """Phase 2実行"""
    # APIキー読み込み
    gemini_key = load_gemini_api_key() if prefer_gemini else None
    claude_key = load_claude_api_key() if not prefer_gemini else None
    
    # Gemini優先、なければClaude
    if prefer_gemini:
        if gemini_key and GEMINI_AVAILABLE:
            print("  ├─ Gemini APIキー読み込み中...")
            print("  │  └─ Gemini APIキー: OK")
            use_gemini = True
        else:
            print("  ├─ Gemini APIキーが見つかりません。Claudeを試します...")
            claude_key = load_claude_api_key()
            if not claude_key:
                print("  ⚠️  Claude APIキーも見つかりません")
                return None
            print("  │  └─ Claude APIキー: OK")
            use_gemini = False
    else:
        print("  ├─ Claude APIキー読み込み中...")
        if not claude_key:
            print("  ⚠️  Claude APIキーが見つかりません")
            return None
        print("  │  └─ Claude APIキー: OK")
        use_gemini = False
    
    # コンセプトを読み込み
    print("  ├─ コンセプト読み込み中...")
    concept_file = project_dir / "01_Research" / "concept_definition.md"
    
    if not concept_file.exists():
        print("  ⚠️  concept_definition.md が見つかりません")
        concept_content = "Threadsで稼ぐ方法"
    else:
        concept_content = concept_file.read_text(encoding="utf-8")
    
    print("  │  └─ コンセプト: OK")
    
    # YouTube動画を検索
    print(f"  ├─ YouTube検索中: 「{keyword}」")
    videos = search_youtube_videos(keyword, max_results=max_videos)
    
    if not videos:
        print("  ⚠️  動画が見つかりませんでした")
        return None
    
    print(f"  │  └─ {len(videos)}件取得")
    
    # yt-dlpのパスを探す
    ytdlp_paths = [
        "/Users/keigo/Library/Python/3.12/bin/yt-dlp",
        "/usr/local/bin/yt-dlp",
        "yt-dlp"
    ]
    
    ytdlp_cmd = None
    for path in ytdlp_paths:
        try:
            result_check = subprocess.run([path, "--version"], capture_output=True, timeout=5)
            if result_check.returncode == 0:
                ytdlp_cmd = path
                break
        except:
            continue
    
    if not ytdlp_cmd:
        print("  ⚠️  yt-dlpが見つかりません")
        return None
    
    # 字幕を取得
    print("  ├─ 字幕取得中...")
    video_data_list = []
    
    for i, video in enumerate(videos, 1):
        print(f"  │  ├─ [{i}/{len(videos)}] {video['title'][:50]}...")
        
        transcript = get_video_transcript(video['id'], ytdlp_cmd)
        
        if transcript:
            video_data_list.append({
                'title': video['title'],
                'views': video['views'],
                'transcript': transcript
            })
            print(f"  │  │  └─ ✅ 字幕取得完了 ({len(transcript)}文字)")
        else:
            print(f"  │  │  └─ ⚠️  字幕なし")
    
    if not video_data_list:
        print("  ⚠️  字幕を取得できた動画がありませんでした")
        return None
    
    print(f"  │  └─ {len(video_data_list)}件の字幕を取得")
    
    # ノウハウ抽出
    if use_gemini:
        print("  ├─ ノウハウ抽出中（Gemini API）...")
        gemini_client = genai.Client(api_key=gemini_key, http_options={"api_version": "v1"})
        knowhow_text, input_tokens, output_tokens = extract_knowhow_with_gemini(
            video_data_list, concept_content, gemini_client
        )
    else:
        print("  ├─ ノウハウ抽出中（Claude API）...")
        claude_client = anthropic.Anthropic(api_key=claude_key)
        knowhow_text, input_tokens, output_tokens = extract_knowhow_with_claude(
            video_data_list, concept_content, claude_client
        )
    
    if not knowhow_text:
        print("  ⚠️  ノウハウ抽出失敗")
        return None
    
    print(f"  │  └─ ノウハウ抽出完了 ({len(knowhow_text)}文字)")
    
    # knowhow_extraction.md を生成
    print("  ├─ knowhow_extraction.md 生成中...")
    research_dir = project_dir / "01_Research"
    research_dir.mkdir(parents=True, exist_ok=True)
    
    knowhow_file = research_dir / "knowhow_extraction.md"
    knowhow_file.write_text(knowhow_text, encoding="utf-8")
    
    print(f"  │  └─ {knowhow_file.name} 保存完了")
    
    print("  └─ Phase 2完了")
    
    return {
        "knowhow_file": str(knowhow_file),
        "videos_found": len(videos),
        "transcripts_retrieved": len(video_data_list),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }
