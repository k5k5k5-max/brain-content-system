"""
Phase 6: Googleドライブアップロード
完成した記事と画像をGoogleドライブにアップロード
"""

from pathlib import Path
from datetime import datetime
import shutil
import os

# Google Drive API
try:
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    import pickle
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    print("⚠️  Google Drive APIパッケージがインストールされていません")

# OAuth 2.0のスコープ
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def get_oauth_credentials(oauth_credentials_path: str = None, token_path: str = None):
    """
    OAuth 2.0認証を行い、認証情報を取得
    
    Args:
        oauth_credentials_path: OAuth 2.0クライアントIDのJSONファイルパス
        token_path: 保存されたトークンのパス
    
    Returns:
        Credentials: 認証情報
    """
    if not oauth_credentials_path:
        oauth_credentials_path = str(Path.home() / ".config" / "gcloud" / "oauth_credentials.json")
    
    if not token_path:
        token_path = str(Path.home() / ".config" / "gcloud" / "token.pickle")
    
    creds = None
    
    # 保存されたトークンを読み込み
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # 認証が必要な場合
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("  │  ├─ トークンを更新中...")
            creds.refresh(Request())
        else:
            if not os.path.exists(oauth_credentials_path):
                raise FileNotFoundError(f"OAuth認証情報が見つかりません: {oauth_credentials_path}")
            
            print("  │  ├─ 初回認証中... ブラウザが開きます")
            flow = InstalledAppFlow.from_client_secrets_file(
                oauth_credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # トークンを保存
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        print("  │  │  └─ トークンを保存しました")
    
    return creds


def upload_to_google_drive(
    project_dir: Path,
    theme_name: str,
    credentials_path: str = None,
    parent_folder_id: str = "1P8RssQ4VfMCmc-cB6NelrAtMKVljNdg_",  # ユーザー提供のフォルダID
    use_oauth: bool = True  # デフォルトでOAuth認証を使用
):
    """
    Googleドライブに記事をアップロード
    
    Args:
        project_dir: プロジェクトディレクトリ（例: 03_Projects/20241210_テーマ名/）
        theme_name: テーマ名
        credentials_path: サービスアカウントJSONファイルのパス（use_oauth=Falseの場合）
        parent_folder_id: アップロード先の親フォルダID
        use_oauth: OAuth認証を使用するか（デフォルト: True）
    
    Returns:
        dict: {
            "success": bool,
            "folder_url": str,
            "uploaded_files": list,
            "error": str (if failed)
        }
    """
    
    print("\n" + "="*60)
    print("📤 Phase 6: Googleドライブアップロード")
    print("="*60)
    
    if not GOOGLE_DRIVE_AVAILABLE:
        return {
            "success": False,
            "error": "Google Drive APIパッケージがインストールされていません"
        }
    
    try:
        # 認証
        if use_oauth:
            print(f"  ├─ OAuth認証中...")
            credentials = get_oauth_credentials()
            print("  │  └─ ✅ 認証成功")
        else:
            # サービスアカウント認証（従来の方法）
            if not credentials_path:
                credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
                if not credentials_path:
                    default_paths = [
                        Path.home() / ".config" / "gcloud" / "brain-drive-service-account.json",
                        Path.cwd() / "brain-drive-credentials.json",
                    ]
                    for path in default_paths:
                        if path.exists():
                            credentials_path = str(path)
                            break
            
            if not credentials_path or not Path(credentials_path).exists():
                print("  ⚠️  Googleドライブ認証情報が見つかりません")
                return {
                    "success": False,
                    "error": "認証情報が見つかりません"
                }
            
            print(f"  ├─ 認証中... ({credentials_path})")
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
            print("  │  └─ ✅ 認証成功")
        
        service = build('drive', 'v3', credentials=credentials)
        
        # 年月フォルダを作成（例: 2024年12月）
        now = datetime.now()
        year_month_folder_name = now.strftime("%Y年%m月")
        
        print(f"  ├─ 年月フォルダを確認中... ({year_month_folder_name})")
        year_month_folder_id = get_or_create_folder(
            service, year_month_folder_name, parent_folder_id
        )
        print(f"  │  └─ ✅ フォルダID: {year_month_folder_id}")
        
        # テーマフォルダを作成（例: 20241210_テーマ名）
        date_prefix = now.strftime("%Y%m%d")
        theme_folder_name = f"{date_prefix}_{theme_name}"
        
        print(f"  ├─ テーマフォルダを作成中... ({theme_folder_name})")
        theme_folder_id = get_or_create_folder(
            service, theme_folder_name, year_month_folder_id
        )
        print(f"  │  └─ ✅ フォルダID: {theme_folder_id}")
        
        # アップロードするファイルを収集
        final_dir = project_dir / "05_Final"
        images_dir = project_dir / "04_Images"
        
        uploaded_files = []
        
        # 1. final_article.md をアップロード
        if (final_dir / "final_article.md").exists():
            print("  ├─ final_article.md アップロード中...")
            file_id = upload_file(
                service,
                final_dir / "final_article.md",
                theme_folder_id,
                "final_article.md"
            )
            uploaded_files.append({"name": "final_article.md", "id": file_id})
            print("  │  └─ ✅ 完了")
        
        # 2. final_article.html をアップロード
        if (final_dir / "final_article.html").exists():
            print("  ├─ final_article.html アップロード中...")
            file_id = upload_file(
                service,
                final_dir / "final_article.html",
                theme_folder_id,
                "final_article.html"
            )
            uploaded_files.append({"name": "final_article.html", "id": file_id})
            print("  │  └─ ✅ 完了")
        
        # 3. 画像フォルダをアップロード
        if images_dir.exists():
            print("  ├─ 画像フォルダをアップロード中...")
            images_folder_id = get_or_create_folder(
                service, "images", theme_folder_id
            )
            
            # 全画像をアップロード
            image_count = 0
            for image_file in images_dir.rglob("*.png"):
                file_id = upload_file(
                    service,
                    image_file,
                    images_folder_id,
                    image_file.name
                )
                uploaded_files.append({"name": f"images/{image_file.name}", "id": file_id})
                image_count += 1
            
            print(f"  │  └─ ✅ {image_count}枚の画像をアップロード完了")
        
        # フォルダのURLを生成
        folder_url = f"https://drive.google.com/drive/folders/{theme_folder_id}"
        
        print("  └─ ✅ アップロード完了")
        print(f"\n📂 Googleドライブ: {folder_url}")
        print("="*60 + "\n")
        
        return {
            "success": True,
            "folder_url": folder_url,
            "folder_id": theme_folder_id,
            "uploaded_files": uploaded_files
        }
    
    except Exception as e:
        print(f"  ❌ エラー: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_or_create_folder(service, folder_name: str, parent_folder_id: str) -> str:
    """
    フォルダを取得または作成
    
    Args:
        service: Google Drive API service
        folder_name: フォルダ名
        parent_folder_id: 親フォルダID
    
    Returns:
        str: フォルダID
    """
    # 既存フォルダを検索
    query = f"name='{folder_name}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if items:
        # 既存フォルダを使用
        return items[0]['id']
    else:
        # 新規フォルダを作成
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')


def upload_file(service, file_path: Path, parent_folder_id: str, file_name: str = None) -> str:
    """
    ファイルをアップロード
    
    Args:
        service: Google Drive API service
        file_path: アップロードするファイルのパス
        parent_folder_id: 親フォルダID
        file_name: アップロード後のファイル名（Noneの場合は元のファイル名）
    
    Returns:
        str: アップロードされたファイルのID
    """
    if not file_name:
        file_name = file_path.name
    
    file_metadata = {
        'name': file_name,
        'parents': [parent_folder_id]
    }
    
    # MIMEタイプを判定
    if file_path.suffix == '.md':
        mime_type = 'text/markdown'
    elif file_path.suffix == '.html':
        mime_type = 'text/html'
    elif file_path.suffix == '.png':
        mime_type = 'image/png'
    elif file_path.suffix == '.jpg' or file_path.suffix == '.jpeg':
        mime_type = 'image/jpeg'
    else:
        mime_type = 'application/octet-stream'
    
    media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    return file.get('id')


def run(project_dir: Path, theme_name: str, config: dict = None):
    """
    Phase 6を実行（メインエントリーポイント）
    
    Args:
        project_dir: プロジェクトディレクトリ
        theme_name: テーマ名
        config: 設定（credentials_pathなど）
    
    Returns:
        dict: アップロード結果
    """
    credentials_path = config.get("google_drive_credentials") if config else None
    parent_folder_id = config.get("google_drive_folder_id", "1P8RssQ4VfMCmc-cB6NelrAtMKVljNdg_") if config else "1P8RssQ4VfMCmc-cB6NelrAtMKVljNdg_"
    
    return upload_to_google_drive(
        project_dir=project_dir,
        theme_name=theme_name,
        credentials_path=credentials_path,
        parent_folder_id=parent_folder_id
    )

