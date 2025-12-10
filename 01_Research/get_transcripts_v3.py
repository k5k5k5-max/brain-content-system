import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcript(video_id):
    try:
        # シンプルなget_transcriptを使用
        # 日本語を優先、なければ英語
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])
        
        # テキスト形式に整形
        formatter = TextFormatter()
        text = formatter.format_transcript(transcript)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    video_ids = [
        "YK-Aj4dGc8w", 
        "t8AXtnHS2b8", 
        "45yDvIJAhTM"
    ]
    
    for vid in video_ids:
        print(f"---START {vid}---")
        result = get_transcript(vid)
        
        # エラーでなければ保存
        if not result.startswith("Error:"):
            with open(f"/Users/keigo/001_cursor/Brain_Content_System_Ver2/03_Projects/20241205_Threads_Monetization/01_Research/youtube_transcripts/{vid}.txt", "w") as f:
                f.write(result)
            print(f"Saved {len(result)} chars to {vid}.txt")
        else:
            print(result)
            
        print(f"---END {vid}---")



