import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcript(video_id):
    try:
        # まず利用可能な字幕リストを取得
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # 日本語字幕を探す（手動字幕または自動生成）
        # find_transcriptは言語コードのリストを受け取る
        transcript = transcript_list.find_transcript(['ja'])
        
        # 字幕データを取得
        transcript_data = transcript.fetch()
        
        # テキスト形式に整形
        formatter = TextFormatter()
        text = formatter.format_transcript(transcript_data)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    video_ids = [
        "YK-Aj4dGc8w", # 動画1
        "t8AXtnHS2b8", # 動画2
        "45yDvIJAhTM"  # 動画3
    ]
    
    for vid in video_ids:
        print(f"---START {vid}---")
        result = get_transcript(vid)
        # 結果が長すぎる場合は先頭の一部と文字数だけ表示（ログ用）
        # 実際にはファイルに保存する方が良いが、今回は標準出力で確認
        print(result[:500] + "..." if len(result) > 500 else result)
        
        # 全文を個別のファイルに保存
        with open(f"/Users/keigo/001_cursor/Brain_Content_System_Ver2/03_Projects/20241205_Threads_Monetization/01_Research/youtube_transcripts/{vid}.txt", "w") as f:
            f.write(result)
            
        print(f"---END {vid}---")



