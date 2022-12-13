# 討厭詭圖鑑 Malicious-project-LineBot
<img src="https://user-images.githubusercontent.com/116346920/207012181-c60c7bb3-d807-484c-b0d0-aeb0506d5b5d.png" width=30%>

## 專案說明
- 討厭詭圖鑑是一個line聊天機器人，透過觀察真假訊息，從中找出相關的語言學特徵。
<img src="https://user-images.githubusercontent.com/116346920/207036936-4c281ef3-05a9-4421-89b9-31ff8bb25057.gif" width=30%>




## 檔案總覽

├── Procfile              # 定義機器人的運行程序
├── README.md                  
├── app.py                # 機器人回應主程式  
└── requirements.txt      # 需求套件

## 檔案說明
- 定義機器人的運行程序 ```procfile``` 
```web: gunicorn py檔名稱:app```
指定gunicorny作為接口，同時開啟多的workers，將用戶送出的request，分流發送給機器人，並能在單個worker無法運作時，自動透過其他worker發送request，以確保運行順暢。


- 機器人回應主程式```app.py```
	- ```app.py```需登入LINE developers填入channel access token和channel secret
	```python=
	# Channel Access Token
	line_bot_api = LineBotApi('ChannelAccessToken')
	# Channel Secret
	handler = WebhookHandler('ChannelSecret')
	```
	- 由關鍵字觸發對應之函式，推進機器人的訊息推播。


## 架設平台
討厭詭圖鑑使用fly.io免付費方案，作為機器人的伺服器。





