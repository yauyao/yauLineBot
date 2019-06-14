from flask import Flask, request, abort
from bs4 import BeautifulSoup
import requests
import os
from ChromeClawer import catchWeb
from Clawer import ticketInfo,imageInfo

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

    else:
        outInfo = ""
        if "!機票" in event.message.text:
            outInfo += ticketInfo

        if "!日幣" in event.message.text:
            resp = requests.get('http://www.findrate.tw/JPY/')
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, 'html.parser')
            first_table = soup.find('table')
            index = 0
            main_tr = first_table.find_all('tr')
            for title in main_tr:
                index = index + 1
                if index == 2:
                    temp = ""
                    tdNum = 0
                    main_td = title.find_all("td")
                    for td in main_td:
                        tdNum = tdNum + 1
                        if tdNum != 4:
                            temp = temp + td.text + "|"

                    temp = temp + "\n"
                    outInfo = outInfo + temp

                if index == 3:
                    temp = ""
                    tdNum = 0
                    main_td = title.find_all("td")
                    for td in main_td:
                        tdNum = tdNum + 1
                        if tdNum != 4:
                            temp = temp + td.text + "|"

                    temp = temp + "\n"
                    outInfo = outInfo + temp
            outInfo = outInfo + "\n連結:http://www.findrate.tw/JPY/"

        if "!美金" in event.message.text:
            resp = requests.get('http://www.findrate.tw/USD/')
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, 'html.parser')
            first_table = soup.find('table')
            index = 0
            main_tr = first_table.find_all('tr')
            for title in main_tr:
                index = index + 1
                if index == 2:
                    temp = ""
                    tdNum = 0
                    main_td = title.find_all("td")
                    for td in main_td:
                        tdNum = tdNum + 1
                        if tdNum != 4:
                            temp = temp + td.text + "|"

                    temp = temp + "\n"
                    outInfo = outInfo + temp

                if index == 3:
                    temp = ""
                    tdNum = 0
                    main_td = title.find_all("td")
                    for td in main_td:
                        tdNum = tdNum + 1
                        if tdNum != 4:
                            temp = temp + td.text + "|"

                    temp = temp + "\n"
                    outInfo = outInfo + temp
            outInfo = outInfo + "\n連結:http://www.findrate.tw/USD/"

        if "!人民幣" in event.message.text:
            resp = requests.get('http://www.findrate.tw/CNY/')
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, 'html.parser')
            first_table = soup.find('table')
            index = 0
            main_tr = first_table.find_all('tr')
            for title in main_tr:
                index = index + 1
                if index == 2:
                    temp = ""
                    tdNum = 0
                    main_td = title.find_all("td")
                    for td in main_td:
                        tdNum = tdNum + 1
                        if tdNum != 4:
                            temp = temp + td.text + "|"

                    temp = temp + "\n"
                    outInfo = outInfo + temp

                if index == 3:
                    temp = ""
                    tdNum = 0
                    main_td = title.find_all("td")
                    for td in main_td:
                        tdNum = tdNum + 1
                        if tdNum != 4:
                            temp = temp + td.text + "|"

                    temp = temp + "\n"
                    outInfo = outInfo + temp
            outInfo = outInfo + "\n連結:http://www.findrate.tw/CNY/"

        if '!測試GO' in event.message.text:
            result = catchWeb()
            print('main:' + result)
            outInfo = outInfo + result

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
