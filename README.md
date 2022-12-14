# 討厭詭圖鑑 Malicious-project-LineBot
<img src="https://user-images.githubusercontent.com/116346920/207012181-c60c7bb3-d807-484c-b0d0-aeb0506d5b5d.png" width=30%>

## 專案說明
- 討厭詭圖鑑是一個line聊天機器人，透過觀察真假訊息，從中找出相關的語言學特徵。
<img src="https://user-images.githubusercontent.com/116346920/207036936-4c281ef3-05a9-4421-89b9-31ff8bb25057.gif" width=30%>

- 歡迎成為討厭詭圖鑑的好友！

<img src="https://user-images.githubusercontent.com/116346920/207417220-a0855683-4435-4c8d-b679-0517aa801e7d.png" width=30%>



## 檔案總覽

├── Procfile　　　　　　　　 # 定義機器人的運行程序<br>
├── README.md                  
├── app.py　　　　　　　　　 # 機器人回應主程式  
└── requirements.txt　　　　# 需求套件

## 檔案說明
- 定義機器人的運行程序 ```procfile``` <br>
```web: gunicorn py檔名稱:app```<br>
指定gunicorny作為接口，同時開啟多的workers，將用戶送出的request，分流發送給機器人，並能在單個worker無法運作時，自動透過其他worker發送request，以確保運行順暢。


- 機器人回應主程式```app.py```
	- ```app.py```需登入LINE developers取得channel access token和channel secret後，填入```app.py```對應欄位，以獲得存取request的權限。



```
# Channel Access Token
line_bot_api = LineBotApi('ChannelAccessToken')
# Channel Secret
handler = WebhookHandler('ChannelSecret')
```

	
[LINE developers](https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2Fchannel%2Fnew%3Ftype%3Dmessaging-api)





## 架設平台
- 由於heroku於2022/11/28取消免付費方案，本專案將伺服器轉移至fly.io，使用免付費方案，作為機器人的伺服器。
- 伺服器部署教學請參考以下連結：

[從Heroku無痛轉移到fly.io，輕鬆部署Python Web專案｜5分鐘學會｜程式設計｜Python｜fly.io部署｜LINEBOT](https://www.youtube.com/watch?v=uqkJmsb8UIY&ab_channel=Maso%E7%9A%84%E8%90%AC%E4%BA%8B%E5%B1%8B)





