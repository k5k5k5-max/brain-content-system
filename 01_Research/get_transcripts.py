import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja'])
        formatter = TextFormatter()
        text = formatter.format_transcript(transcript)
        return text
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    video_ids = [
        "YK-Aj4dGc8w", # 動画1
        "t8AXtnHS2b8", # 動画2
        "45yDvIJAhTM"  # 動画3
    ]
    
    for vid in video_ids:
        print(f"---START {vid}---")
        print(get_transcript(vid))
        print(f"---END {vid}---")



