from googleapiclient.discovery import build
import json

API_KEY = "AIzaSyArNfnF3GBFp5TU5U-iYjxBsGbzvAvoCxU"
CAPTION_ID = "AUieDaYFpVDtWMXTUdtPcu-BZoVzN4-9R4duh3J4Hu9ytchuO-M"

def download_caption():
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        # 字幕データをダウンロード (tfmt='srt' 推奨)
        request = youtube.captions().download(
            id=CAPTION_ID,
            tfmt='srt' 
        )
        # バイナリデータとして取得
        response = request.execute()
        
        return response.decode('utf-8')

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    text = download_caption()
    
    # 結果を保存
    if not text.startswith("Error:"):
        with open("/Users/keigo/001_cursor/Brain_Content_System_Ver2/01_Research/youtube_transcripts/YK-Aj4dGc8w.srt", "w") as f:
            f.write(text)
        print("Download successful!")
        print(text[:500] + "...")
    else:
        print(text)



