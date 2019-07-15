from flask import Flask, request, abort
import os
from service.ChromeClawer import catchWeb
from service.Clawer import ticketInfo,imageInfo,exchangeRate,fruitPrice,getImage,getHtmlImgUrl,getSebUrl

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ['LINE_ACCESS_TOKEN'])
# Channel Secret
handler = WebhookHandler(os.environ['LINE_SECRET'])

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    print("on Call"+event.message.text)

    if "https://www.instagram.com" in event.message.text:
        # 返回含圖片Message
        imageUrl = ""
        imageUrl += imageInfo(event.message.text)

        if imageUrl != "":
            message = ImageSendMessage(
                original_content_url=imageUrl,
                preview_image_url=imageUrl
            )
            line_bot_api.reply_message(
                event.reply_token,
                message)

    if '!妹子' in event.message.text:
        imageUrl = getImage(getHtmlImgUrl(getSebUrl('https://www.mzitu.com/')))
        if imageUrl != "":
            message = ImageSendMessage(
                original_content_url=imageUrl,
                preview_image_url=imageUrl
            )
            line_bot_api.reply_message(
                event.reply_token,
                message)

    else:
        # 返回純文字Message
        outInfo = ""
        if "!機票" in event.message.text:
            outInfo += ticketInfo()

        if "!日幣" in event.message.text:
            outInfo += exchangeRate("JPY")

        if "!美金" in event.message.text:
            outInfo += exchangeRate("USD")

        if "!人民幣" in event.message.text:
            outInfo += exchangeRate("CNY")

        if "!歐元" in event.message.text:
            outInfo += exchangeRate("EUR")

        if "!英鎊" in event.message.text:
            outInfo += exchangeRate("GBP")

        if '!測試GO' in event.message.text:
            result = catchWeb()
            print('main:' + result)
            outInfo += result

        if '!奶子' in event.message.text:
            outInfo += "沒有女乃豆頁大 自己生"

        if '!火龍果' in event.message.text:
            outInfo += fruitPrice("812/%E7%81%AB%E9%BE%8D%E6%9E%9C-%E7%B4%85%E8%82%89(%E7%B4%85%E9%BE%8D%E6%9E%9C")


        print("outInfo:" + outInfo)

        if outInfo!="":
            message = TextSendMessage(text=outInfo)
            line_bot_api.reply_message(
                event.reply_token,
                message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
