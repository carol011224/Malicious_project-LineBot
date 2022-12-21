# 討厭詭圖鑑 Malicious-project-LineBot
<img src="https://user-images.githubusercontent.com/116346920/207012181-c60c7bb3-d807-484c-b0d0-aeb0506d5b5d.png" width=30%>

## 專案說明
- 討厭詭圖鑑是一個 LINE 聊天機器人，透過觀察真假訊息，從中找出相關的語言學特徵。
<img src="https://user-images.githubusercontent.com/116346920/207036936-4c281ef3-05a9-4421-89b9-31ff8bb25057.gif" width=30%>

- 歡迎成為討厭詭圖鑑的好友！

<img src="https://user-images.githubusercontent.com/116346920/207417220-a0855683-4435-4c8d-b679-0517aa801e7d.png" width=30%>



## 檔案總覽

```
├── Procfile                # 定義機器人的運行程序
├── README.md               # 專案說明
├── app.py                  # 機器人回應主程式
└── requirements.txt        # 需求套件
```
## 檔案說明
-  `procfile` ：定義機器人的運行程序

指定 gunicorn 作為接口，指定型別為`app`，同時開啟多的 workers，將用戶送出的 request，分流發送給機器人，並能在單個 worker 無法運作時，自動透過其他 worker 發送 request，以確保運行順暢。

[gunicorn 操作說明](https://devcenter.heroku.com/articles/python-gunicorn)

- `app.py` ：機器人主程式
	- 機器人訊息的模板及 LINE developers 可以參考[yaoandy107/line-bot-tutorial](https://github.com/yaoandy107/line-bot-tutorial)的作法。
	- 登入 [LINE developers](https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2Fchannel%2Fnew%3Ftype%3Dmessaging-api) 取得 Channel Access Token 和 Channel Secret 後，填入`app.py`對應欄位，以獲得存取 request 的權限。

	
```py
# Channel Access Token
line_bot_api = LineBotApi('ChannelAccessToken')
# Channel Secret
handler = WebhookHandler('ChannelSecret')
```

	


- `requirements.txt` ：機器人需要安裝的套件

```
line-bot-sdk
flask
gunicorn
```

## 伺服器架設

- 我們選用fly.io做為機器人的架設平台，架設的方式可以參考[這個影片](https://www.youtube.com/watch?v=uqkJmsb8UIY&ab_channel=Maso%E7%9A%84%E8%90%AC%E4%BA%8B%E5%B1%8B)。









