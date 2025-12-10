from googleapiclient.discovery import build
import json

API_KEY = "AIzaSyArNfnF3GBFp5TU5U-iYjxBsGbzvAvoCxU"
VIDEO_ID = "YK-Aj4dGc8w"

def check_captions():
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        # 字幕トラックのリストを取得
        request = youtube.captions().list(
            part="snippet",
            videoId=VIDEO_ID
        )
        response = request.execute()
        
        return response

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = check_captions()
    print(json.dumps(result, indent=2, ensure_ascii=False))



