import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 定义作用域和凭据文件路径
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = "/home/cofincup/Documents/auth/client_secret_805207980404-sod9j5n2bjl9lgk25569a8oj3meqopo3.apps.googleusercontent.com.json"
TOKEN_PICKLE_FILE = 'token.pickle'

def authenticate():
    creds = None

    # 加载已保存的访问令牌
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)

    # 如果没有有效的凭据，则进行身份验证
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=56115)
        # 保存访问令牌供以后使用
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_unread_count():
    creds = authenticate()

    # 创建Gmail服务对象
    service = build('gmail', 'v1', credentials=creds)

    # 获取未读邮件数量
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    unread_count = results.get('resultSizeEstimate', 0)

    return unread_count

# 调用函数并打印未读邮件数量
unread_count = get_unread_count()
print('----------------------------')
print('今日Gmail未读邮件数量:', unread_count)
print('----------------------------')
