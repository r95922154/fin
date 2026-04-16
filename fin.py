import requests
#import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")
RATE =[]

# =========================
# 匯率
# =========================
def get_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/TWD"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        jpy = data["rates"]["JPY"]
        usd = data["rates"]["USD"]

        RATE.append(f"台/日: {jpy:.4f}")
        RATE.append(f"美/台: {1/usd:.4f}")
        RATE.append(f"美/日: {jpy/usd:.4f}")

    except Exception as e:
        RATE.append(f"匯率取得失敗: {e}")
        

# =========================
# 原油價格
# =========================
def get_oil_price():
    symbols = {
        "WTI原油": "CL=F",
        "布蘭特原油": "BZ=F"
    }

    for name, symbol in symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")

            if hist.empty:
                RATE.append(f"{name}: 無資料")
                continue

            price = hist["Close"].iloc[-1]
            now = datetime.now().strftime("%Y-%m-%d %H:%M")

            RATE.append(f"{name}: {price:.2f} ({now})")

        except Exception as e:
            RATE.append(f"{name} 取得失敗: {e}")



# =========================
# 股票價格
# =========================
def get_stock_data():
    stocks = {
        "2330.TW": "台積電",
        "0050.TW": "元大台灣50",
        "2317.TW": "鴻海",
        "6547.TWO": "高端疫苗"
    }

    for symbol, name in stocks.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")

            if len(hist) < 2:
                RATE.append(f"{name}: 無資料")
                continue

            close_today = hist["Close"].iloc[-1]
            close_yesterday = hist["Close"].iloc[-2]

            diff = close_today - close_yesterday
            pct = (diff / close_yesterday) * 100

            sign = "+" if diff > 0 else ""

            RATE.append(
                f"{name}: {close_today:.2f} ({sign}{diff:.2f}, {sign}{pct:.2f}%)"
            )

        except Exception as e:
            RATE.append(f"{name} 取得失敗: {e}")



# =========================
# 發送 LINE
# =========================
def send_message_to_line():
    # LINE Messaging API 設定
    LINE_API_URL = "https://api.line.me/v2/bot/message/push"

    # 設定要發送的訊息內容
    message = "\n".join(RATE)
    payload = {
        "to": TO_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    # 設定 HTTP 請求的標頭
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # 發送 POST 請求
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print("LINE 發送成功:", response.text)

    except Exception as e:
        print("LINE 發送失敗:", e)


# =========================
# 主程式
# =========================
def sendlist():
    RATE.clear()

    get_exchange_rate()
    get_oil_price()
    #get_stock_data()

    send_message_to_line()


if __name__ == "__main__":
    sendlist()
