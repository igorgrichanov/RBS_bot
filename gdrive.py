
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import os
import pprint
import io

import config

pp = pprint.PrettyPrinter(indent=4)

SERVICE_ACCOUNT_FILE = os.path.abspath(__file__)[:-9] + config.SERVICE_ACCOUNT_FILE

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=config.SCOPES)
service = build(config.API_NAME, config.API_VERSION, credentials=credentials)

def create_orgs_folder(name, folder_id):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    r = service.files().create(body=file_metadata, fields='id').execute()

    return r["id"]

def drive_upload(file_path, file_name, folder_id):
    if folder_id == "0":
        folder_id = config.folder_id
    file_metadata = {'name': file_name,
                    'parents': [folder_id] }
    
    # permissions_d = {'allowFileDiscovery': False,
    #                 'id': 'anyoneWithLink',
    #                 'kind': 'drive#permission',
    #                 'role': 'reader',
    #                 'type': 'anyone'}
    print(file_path)
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='webViewLink').execute()
    # r = service.files().create(body=file_metadata, media_body=media, fields='webViewLink', permissions = permissions_d).execute()

def drive_download(file_name, file_id):
    # file_id = '1HKC4U1BMJTsonlYJhUKzM-ygrIVGzdBr'
    request = service.files().get_media(fileId=file_id)
    filename = '/home/makarov/File.csv'
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))


def drive_get_folder(folder_id, find_folder):
    
    # results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name, mimeType)").execute()
    results = service.files().list(pageSize=5, fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",q="'" + folder_id + "' in parents").execute()
    # print(results)
    # pp.pprint(results['files'])
    for x in results['files']:
        if find_folder in x['name']:
            return x['id']
    
# drive_upload(os.path.abspath(__file__), "asdfasdf.txt")
# drive_get_folder("1SbBv3Wq0-Q_kWm8eYntoEJWrm_Uu57AP", "sdfg")
# drive_get_folder(config.folder_id, "sdfg")

def drive_check_all(folder_id):
    results = service.files().list(pageSize=5, fields="nextPageToken, files(id, name, mimeType, parents, createdTime, permissions)",q="'" + folder_id + "' in parents").execute()
    return results

# # # r = drive_check_all("1ZCtRa5hlpkIqqlJwxr2iHQlRs8FrOtSD")
# # r = drive_check_all("1wOLKaAQr7S27kUi3aDQxuQFw7hIUGDQQ")
# r = drive_check_all("1wOLKaAQr7S27kUi3aDQxuQFw7hIUGDQQ")
# # print(r)
# pp.pprint(r['files'])
# for x in r['files']:
#     if "plain" in x['mimeType'] or "document" in x['mimeType']:
#         print("============")
#         print(x['name'])
#         print(x['id'])


# def drive_get_all_docs(folder_id):
#     f1 = drive_get_folder(folder_id, "Трудоустройство")
#     f2 = drive_get_folder(folder_id, "Финансовые документы")
#     res_list1 = drive_check_all(f1)
#     res_list2 = drive_check_all(f2)
#     res_l = list()
#     try:
#         res_l.append()
#     except:
#         None





