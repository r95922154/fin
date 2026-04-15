import requests

# LINE Messaging API 設定
LINE_API_URL = "https://api.line.me/v2/bot/message/push"
ACCESS_TOKEN = '7zBuWUKv+7LgMvwa9MAMNpwuFvKhttN/GmrxlIQ9GFuV8bvEZ6HVJyCGqafbbxIe7TJpL0fafqEP6LjdJheE5c2U/xz5OnaCnMQVw9rQpucf2Z9+OKocwceJ5NFfLaVgddcfzyXRTeAimkPlkj+utQdB04t89/1O/w1cDnyilFU='  # 在這裡填入你的 Channel Access Token
USER_ID = 'U35b44a804caf582e8674bbf9d49f5962'  # 在這裡填入你要發送訊息的使用者的 LINE ID

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
