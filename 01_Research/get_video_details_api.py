from googleapiclient.discovery import build
import json

API_KEY = "AIzaSyArNfnF3GBFp5TU5U-iYjxBsGbzvAvoCxU"
VIDEO_IDS = ["YK-Aj4dGc8w", "t8AXtnHS2b8", "45yDvIJAhTM"]

def get_video_details():
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(VIDEO_IDS)
        )
        response = request.execute()
        
        results = []
        for item in response.get("items", []):
            snippet = item["snippet"]
            video_data = {
                "id": item["id"],
                "title": snippet["title"],
                "description": snippet["description"],
                "tags": snippet.get("tags", []),
                "channelTitle": snippet["channelTitle"],
                "viewCount": item["statistics"].get("viewCount"),
                "likeCount": item["statistics"].get("likeCount")
            }
            results.append(video_data)
            
        return results

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    data = get_video_details()
    
    # 結果を表示＆保存
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    with open("/Users/keigo/001_cursor/Brain_Content_System_Ver2/01_Research/youtube_api_details.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



