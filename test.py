
# from Google import Create_Service
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import os
import pprint
import io


SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.path.abspath(__file__)[:-7] + "apt-federation-388707-ed1d0657503a.json"
id_folder = "1YM9sE-M4Gl7WWms0NTIMT5svLivMZjSu"
API_NAME = "drive"
API_VERSION = "v3"

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build(API_NAME, API_VERSION, credentials=credentials)

results = service.files().list(pageSize=10,
                               fields="nextPageToken, files(id, name, mimeType)").execute()


print(type(results))
for x in results["files"]:
    print(x)

name = "Договор куплипродажи-продажи (шаблон).docx"
file_path = os.path.abspath(__file__)

file_metadata = {
                'name': name,
                'parents': [id_folder]
            }
media = MediaFileUpload(file_path, resumable=True)
# rrr = service.files().create(body=file_metadata, media_body=media, fields='webViewLink').execute()



# folder_id = '1uuecd6ndiZlj3d9dSVeZeKyEmEkC7qyr'
name = 'sdfgQQQ'
file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [id_folder]
}
r = service.files().create(body=file_metadata, fields='id').execute()

print(r)
print(type(r))
print(r["id"])
