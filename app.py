from flask import Flask, request, abort
from bs4 import BeautifulSoup
import requests


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
line_bot_api = LineBotApi('XOVtTRKkreHUr1XhwbR1M1RAAC4ZBHekThLI2rHNjBMCC8zHXGnwHmyJWPccNSUE1p06TKLhIHXMq+gCMspwcu8Z/UzBFDDIvkluahnupCfROwZtYS8duznXojwcljBQvzTQThwsnBwzoY4S0fh7UQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('895c0915980750bb7f8ce330b1143e56')

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
    resp = requests.get('https://www.ptt.cc/bbs/Japan_Travel/index.html')
    soup = BeautifulSoup(resp.text, 'html.parser')

    main_titles = soup.find_all('div', 'title')
    for title in main_titles:

        if "資訊" in title.text:
            print(title.text.strip())
            print("https://www.ptt.cc" + title.find("a")['href'])

    print("event.message.text"+event.message.text+"@@@\nmessage"+event.message)
    app.logger.info("event.message.text"+event.message.text+"@@@\nmessage"+event.message)

    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
