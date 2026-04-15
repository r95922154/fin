import requests
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")

print(ACCESS_TOKEN)
print("/n")
print(USER_ID)


# LINE Messaging API 設定
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

# 設定要發送的訊息內容
message = {
    "to": USER_ID,
    "messages": [
        {
            "type": "text",
            "text": "這是從發送到 LINE 的訊息！"
        }
    ]
}

# 設定 HTTP 請求的標頭
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# 發送 POST 請求
response = requests.post(LINE_API_URL, json=message, headers=headers, verify=False)

# 顯示回應結果
if response.status_code == 200:
    print("訊息發送成功！")
else:
    print(f"發送失敗，錯誤代碼: {response.status_code}")
    print(response.text)
