import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import dateutil.parser as parser
import base64
import json

CREDENTIALS_PATH = './credentials.json'                     # 認証情報が記載されたjsonファイルへのパス
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] # スコープ（権限）

class GmailService:
    def __init__(self):
        self.credentials = self.get_credentials()
        self.service = build('gmail', 'v1', credentials = self.credentials)

    # 認証情報を取得
    def get_credentials(self):
        credentials = None

        # トークンを含んだpickleファイルが存在する場合はそれを使用
        if os.path.exists('./token.pickle'):
            with open('./token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        # トークンを含んだpickleファイルが存在しない（有効でない）場合は作成（更新）
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                credentials = flow.run_local_server()

            with open('./token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
        
        return credentials
    
    # Gmail APIを叩いてメッセージを取得
    def get_messages(self, max_results = 5, q = ''):
        print('Gmailから未読メッセージを取得中...')

        messages = self.service.users().messages()
        messages_list = messages.list(
            userId = 'me',
            labelIds = ['UNREAD'],   # ラベル（今回は「未読」を指定）
            maxResults = max_results, # 最大取得件数
            q = q                    # クエリ（from、to、after、beforeなど）
        ).execute()

        # メッセージが1件も無かった場合はNoneを返す
        if 'messages' not in messages_list: return None

        dicts = []

        for message in messages_list['messages']:
            # idをもとにメッセージの詳細を取得
            message_detail = messages.get(userId = 'me', id = message['id']).execute()

            dict = {}

            dict['id'] = message['id']
            
            # ヘッダー部分（日付、差出人、宛先、件名）
            for header in message_detail['payload']['headers']:
                if header['name'] == 'Date':
                    dict['date'] = parser.parse(header['value']).strftime('%Y/%m/%d %H:%M')
                elif header['name'] == 'From':
                    dict['from'] = header['value']
                elif header['name'] == 'To':
                    dict['to'] = header['value']
                elif header['name'] == 'Subject':
                    if header['value'] != '':
                        dict['subject'] = header['value']
                    else:
                        dict['subject'] = '件名なし'
            
            # 本文の概要
            if message_detail['snippet'] != '':
                dict['snippet'] = message_detail['snippet']
            else:
                dict['snippet'] = '本文なし'

            dicts.append(dict)
 
        return json.dumps(dicts, ensure_ascii = False)
