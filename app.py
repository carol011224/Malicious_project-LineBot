from flask import Flask, request, abort


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import re

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ChannelAccessToken')
# Channel Secret
handler = WebhookHandler('ChannelSecret')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)

def prettyEcho0(event):
    input_string = event.message.text
    if "開始挑戰" in input_string:
        message = startaction()
    elif "第一題" in input_string:
        message = prettyEcho1(input_string)
    elif "第二題" in input_string:
        message = prettyEcho2(input_string)
    elif "第三題" in input_string:
        message = prettyEcho3(input_string)
    line_bot_api.reply_message(event.reply_token, message)

def prettyEcho1(input_string):
    #input_string=event.message.text

    if "第一題答對！！" in input_string:
        message = corr_answer()        
    elif "第一題答錯嗚嗚..." in input_string:
        message = incorr_answer()    
    elif "第一題的討厭詭在哪裡咧？！" in input_string:
        message = feat()
    elif "我覺得第一題的討厭詭是 A C D E" in input_string:
        message = feat_corr()
    elif "我覺得第一題的討厭詭是" in input_string:
        message = feat_incorr()    
    elif "第一題的討厭詭快現形吧！" in input_string:
        message = explain()
    elif "第一題結束～～再玩一題" in input_string:
        message = news2()
    #line_bot_api.reply_message(event.reply_token, message)
    return message

def prettyEcho2(input_string):
    #input_string=event.message.text
    
    if "第二題答對！！" in input_string:
        message = corr_answer2()
    elif "第二題答錯嗚嗚..." in input_string:
        message = incorr_answer2()    
    elif "第二題的討厭詭在哪裡咧？！" in input_string:
        message = feat2()
    elif "我猜第二題的討厭詭是 B C D" in input_string:
        message = feat_corr2()
    elif "我猜第二題的討厭詭是" in input_string:
        message = feat_incorr2()    
    elif "第二題的討厭詭還不現形啊！" in input_string:
        message = explain2()
    elif "第二題結束～～再玩一題" in input_string:
        message = news3()
    #line_bot_api.reply_message(event.reply_token, message)
    return message

def prettyEcho3(input_string):
    #input_string=event.message.text
    
    if "第三題答對！！" in input_string:
        message = corr_answer3()
    elif "第三題答錯嗚嗚..." in input_string:
        message = incorr_answer3()    
    elif "第三題的討厭詭在哪裡咧？！" in input_string:
        message = feat3()
    elif "第三題的討厭詭應該是 A B C E" in input_string:
        message = feat_corr3()
    elif "第三題的討厭詭應該是" in input_string:
        message = feat_incorr3()    
    elif "出來吧！第三題的討厭詭" in input_string:
        message = explain3()   
    else:
        message = TextSendMessage(text="很抱歉...我聽不懂啊～～")
    return message

#start 
def startaction():
    reply_arr=[]
    reply_arr.append(TextSendMessage(text='蒐集討厭詭的任務即將開始！！\n任務內容：破解三題假新聞並仔細尋找哪些句子藏有假訊息的特徵。\n抓出討厭詭的任務就交給你了💪💪'))
    reply_arr.append(TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/WcWii1z.png',
                title='訊息一',
                text=' ',
                actions=[
                    MessageTemplateAction(
                        label='這篇是假訊息！',
                        text='第一題答錯嗚嗚...' #需要修改
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/M785WId.png',
                title='訊息二',
                text=' ',
                actions=[
                    MessageTemplateAction(
                        label='這篇是假訊息！',
                        text='第一題答對！！' #需要修改
                    )
                ]
            )
        ]
    )
))
    #line_bot_api.reply_message(event.reply_token, reply_arr)
    return reply_arr
    



def news2():
    newsMSG = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/COGBqSm.png',
                    title='訊息ㄧ',
                    text=' ',
                    actions=[
                        MessageTemplateAction(
                            label='這篇是假訊息！',
                            text='第二題答對！！' #需要修改
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/C6TU1aP.png',
                    title='訊息二',
                    text=' ',
                    actions=[
                        MessageTemplateAction(
                            label='這篇是假訊息！',
                            text='第二題答錯嗚嗚...'#需要修改
                        )
                    ]
                )
            ]
        )
    )
    return newsMSG

def news3():
    newsMSG = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/t4ypv0k.png',
                    title='訊息一',
                    text=' ',
                    actions=[
                        MessageTemplateAction(
                            label='這篇是假訊息！',
                            text='第三題答錯嗚嗚...'#需要修改
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/vOM3cGE.png',
                    title='訊息二',
                    text=' ',
                    actions=[
                        MessageTemplateAction(
                            label='這篇是假訊息！',
                            text='第三題答對！！'#需要修改
                        )
                    ]
                )
            ]
        )
    )
    return newsMSG

#correct answer
def corr_answer():
    corr_answerMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/M785WId.png',
            text='恭喜答對啦！！！此篇為假訊息。',
            actions=[
                MessageTemplateAction(
                    label='點我開始找討厭詭',
                    text='第一題的討厭詭在哪裡咧？！'
                )
            ]
        )
    )
    return corr_answerMSG

def corr_answer2():
    corr_answerMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/G82hUBM.png',
            text='恭喜答對啦！！！此篇為假訊息。',
            actions=[
                MessageTemplateAction(
                    label='點我開始找討厭詭',
                    text='第二題的討厭詭在哪裡咧？！'
                )
            ]
        )
    )
    return corr_answerMSG

def corr_answer3():
    corr_answerMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/wHrnxrp.png',
            text='恭喜答對啦！！！此篇為假訊息。',
            actions=[
                MessageTemplateAction(
                    label='點我開始找討厭詭',
                    text='第三題的討厭詭在哪裡咧？！'
                )
            ]
        )
    )
    return corr_answerMSG

#incorrect answer
def incorr_answer():
    incorr_answerMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/M785WId.png',
            text='嗚嗚...答錯啦！！！此篇才是假訊息。',
            actions=[
                MessageTemplateAction(
                    label='點我開始找討厭詭',
                    text='第一題的討厭詭在哪裡咧？！'
                )
            ]
        )
    )
    return incorr_answerMSG

def incorr_answer2():
    incorr_answerMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/G82hUBM.png',
            text='嗚嗚...答錯啦！！！此篇才是假訊息。',
            actions=[
                MessageTemplateAction(
                    label='點我開始找討厭詭',
                    text='第二題的討厭詭在哪裡咧？！'
                )
            ]
        )
    )
    return incorr_answerMSG

def incorr_answer3():
    incorr_answerMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/wHrnxrp.png',
            text='嗚嗚...答錯啦！！！此篇才是假訊息。',
            actions=[
                MessageTemplateAction(
                    label='點我開始找討厭詭',
                    text='第三題的討厭詭在哪裡咧？！'
                )
            ]
        )
    )
    return incorr_answerMSG

#feature
def feat():
    feat_MSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/G0MwsiV.png',
            text='這篇文章有哪些討厭詭呢？',
            actions=[
                MessageTemplateAction(
                    label='A B C E',
                    text='我覺得第一題的討厭詭是 A B C E'
                ),
                MessageTemplateAction(
                    label='A C D E',
                    text='我覺得第一題的討厭詭是 A C D E'
                ),
                MessageTemplateAction(
                    label='D E',
                    text='我覺得第一題的討厭詭是 D E'
                )                
            ]
        )
    )
    return feat_MSG

def feat2():
    feat_MSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/m83diXk.png',
            text='這篇文章有哪些討厭詭呢？',
            actions=[
                MessageTemplateAction(
                    label='A B C',
                    text='我猜第二題的討厭詭是 A B C'
                ),
                MessageTemplateAction(
                    label='B C D',
                    text='我猜第二題的討厭詭是 B C D'
                ),
                MessageTemplateAction(
                    label='A',
                    text='我猜第二題的討厭詭是 A'
                )                
            ]
        )
    )
    return feat_MSG

def feat3():
    feat_MSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/WxseYbC.png',
            text='這篇文章有哪些討厭詭呢？',
            actions=[
                MessageTemplateAction(
                    label='A B C E',
                    text='第三題的討厭詭應該是 A B C E'
                ),
                MessageTemplateAction(
                    label='B D F',
                    text='第三題的討厭詭應該是 B D F'
                ),
                MessageTemplateAction(
                    label='C E F',
                    text='第三題的討厭詭應該是 C E F'
                )                
            ]
        )
    )
    return feat_MSG


#feature-correct answer
def feat_corr():
    feat_corrMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/uJpW26D.jpg',
            text='恭喜答對啦！！！\n答案是 A C D E',
            actions=[
                MessageTemplateAction(
                    label='討厭詭現形',
                    text='第一題的討厭詭快現形吧！'
                )
            ]
        )
    )
    return feat_corrMSG

def feat_corr2():
    feat_corrMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/uJpW26D.jpg',
            text='恭喜答對啦！！！\n答案是 B C D',
            actions=[
                MessageTemplateAction(
                    label='討厭詭現形',
                    text='第二題的討厭詭還不現形啊！'
                )
            ]
        )
    )
    return feat_corrMSG

def feat_corr3():
    feat_corrMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/uJpW26D.jpg',
            text='恭喜答對啦！！！\n答案是 A B C E',
            actions=[
                MessageTemplateAction(
                    label='討厭詭現形',
                    text='出來吧！第三題的討厭詭'
                )
            ]
        )
    )
    return feat_corrMSG



#feature-incorrect answer
def feat_incorr():
    feat_incorrMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/VvMWun9.jpg',
            text='嗚嗚...差一點就找出討厭詭啦！！！答案是 A C D E',
            actions=[
                MessageTemplateAction(
                    label='討厭詭現形',
                    text='第一題的討厭詭快現形吧！'
                )
            ]
        )
    )
    return feat_incorrMSG

def feat_incorr2():
    feat_incorrMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/VvMWun9.jpg',
            text='嗚嗚...差一點就找出討厭詭啦！！！答案是 B C D',
            actions=[
                MessageTemplateAction(
                    label='討厭詭現形',
                    text='第二題的討厭詭還不現形啊！'
                )
            ]
        )
    )
    return feat_incorrMSG


def feat_incorr3():
    feat_incorrMSG = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/VvMWun9.jpg',
            text='嗚嗚...差一點就找出討厭詭啦！！！答案是 A B C E',
            actions=[
                MessageTemplateAction(
                    label='討厭詭現形',
                    text='出來吧！第三題的討厭詭'
                )
            ]
        )
    )
    return feat_incorrMSG


#explanation
def explain():
    explainMSG = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/Y4egWBW.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                 actions=[
                    MessageAction(
                        label='下一題',
                        text='第一題結束～～再玩一題' #需要修改
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/CUohuAh.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                actions=[
                    MessageAction(
                        label='下一題',
                        text='第一題結束～～再玩一題' #需要修改
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/9jROrwE.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                actions=[
                    MessageAction(
                        label='下一題',
                        text='第一題結束～～再玩一題' #需要修改
                    )
                ]
            )            
        ]
    )
)
    return explainMSG


def explain2():
    explainMSG = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/OzVbOES.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                 actions=[
                    MessageAction(
                        label='下一題',
                        text='第二題結束～～再玩一題' #需要修改
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/6EeVp9h.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                actions=[
                    MessageAction(
                        label='下一題',
                        text='第二題結束～～再玩一題' #需要修改
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/yqNx9ys.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                actions=[
                    MessageAction(
                        label='下一題',
                        text='第二題結束～～再玩一題' #需要修改
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/3YAngGY.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                actions=[
                    MessageAction(
                        label='下一題',
                        text='第二題結束～～再玩一題' #需要修改
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/mJjvx3I.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                actions=[
                    MessageAction(
                        label='下一題',
                        text='第二題結束～～再玩一題' #需要修改
                    )
                ]
            )            
        ]
    )
)
    return explainMSG


def explain3():
    explainMSG = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/P3VwPNC.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                 actions=[
                    MessageAction(
                        label='任務完成～～再挑戰一次',
                        text='開始挑戰'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/rftwpTg.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                actions=[
                    MessageAction(
                        label='任務完成～～再挑戰一次',
                        text='開始挑戰'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/56Ec15z.png',
                title='假訊息特徵',
                text='如果文字中出現了這個特徵，就有可能是假訊息喔！',
                actions=[
                    MessageAction(
                        label='任務完成～～再挑戰一次',
                        text='開始挑戰'
                    )
                ]
            )            
        ]
    )
)
    return explainMSG



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
