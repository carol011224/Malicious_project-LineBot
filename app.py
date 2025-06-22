import os
import json
import requests
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from marker import analyze_markers



# 載入環境變數
load_dotenv()
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("🔧 LINE_SECRET:", LINE_CHANNEL_SECRET)
print("🔧 LINE_TOKEN:", LINE_CHANNEL_ACCESS_TOKEN)
print("🔧 GEMINI_API_KEY:", GEMINI_API_KEY)



# Gemini API 設定
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def call_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("❌ Gemini 錯誤：", e)
        return "抱歉，我暫時無法回應。"

app = Flask(__name__)
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("🪵 webhook 被呼叫了")
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    print("📩 收到訊息：", body)
    print("📩 簽名：", signature)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("❌ Webhook 處理錯誤：", e)
        abort(400)
    
    return "OK"


# 文字訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
#### 接收訊息
    print("✅ 成功觸發 handler.add 的回應處理！")
    user_input = event.message.text
    marker_info=analyze_markers(user_input)
    print("🗣 使用者輸入：", user_input)
    print("⚙️ marker 分析：", marker_info)
#### 將訊息送進gemini，透過prompt設計，讓他根據 Metadiscourse 去分析
    prompt = f"""
你是一名語言學專家，你擅長的領域是 metadiscourse 的分析。
metadiscourse 中的 interactional markers 包含以下五類：

- hedge：作者表達對命題的不確定性，有討論空間
- booster：作者表達對命題的確定性，沒有任何討論空間
- attitude：作者對命題的態度和看法，包含驚訝、義務、認同、重要性等
- self-mention：作者明確在文章內提及自己
- engagement：提及讀者，或是將讀者一起納入情境中

你現在的任務是：**根據使用者提供的輸入訊息，結合這些 interactional markers 的出現情形，分析這段訊息是否具有誤導、操弄或非中立的語氣特徵。**

---

使用者輸入如下：
{user_input}

系統根據關鍵詞比對結果，提供以下分析結構（每一類包含出現次數、實際出現的詞，以及出現比例）：
（資料格式為 JSON，其中每個 marker 類別包含以下欄位：

- `count`：該類型 marker 出現的次數
- `words`：實際出現的 marker 詞語
- `ratio`：該類型 marker 出現次數佔整體詞語數的比例（四捨五入至小數點第四位）

另外，最下方的 `total_ratio` 表示所有 interactional markers 出現次數的總和，佔總字詞數的比例，可用來評估整體語氣的操作性程度。


{json.dumps(marker_info, ensure_ascii=False, indent=2)}

---

生成回應時必須遵守以下規則。
- ❗ 只需要分析 marker，你只需要指出語氣風格是否有需要注意的地方。
- 使用者是一般民眾，不需提及理論內容。
- 不要說出 marker 的比例，這個比例是提供給你判斷的。
- 不要點出 marker 名稱，請直接指出出現的詞，並用自然語氣做簡短說明。
- 不提及未出現的 marker（即 `count`=0 的部分）。
- 不使用 Markdown 或 HTML。
- 每個說明請控制在 50 字以內，總長度控制在 5 則簡要描述以內。
- 請避免使用「標記詞語」、「標記語」、 interactional marker 或 metadiscourse 等術語。請改用「語氣用詞」等使用者較易理解的詞彙。
- 請在結尾提醒：這些分析僅針對語氣用詞，並不等同於內容真偽，建議搭配查證。


現在以「讓我們來看看有哪些地方需要特別注意！」開頭，開始生成回應。
"""

#### 生成回應
    gemini_answer = call_gemini(prompt)
    answer =gemini_answer
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=answer)]
            )
        )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port)
