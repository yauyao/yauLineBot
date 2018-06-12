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
    outInfo = ""
    print("on Call"+event.message.text)
    if "!機票" in event.message.text:
        resp = requests.get('https://www.ptt.cc/bbs/Japan_Travel/index.html')
        soup = BeautifulSoup(resp.text, 'html.parser')
        main_titles = soup.find_all('div', 'title')

        for title in main_titles:

            if "資訊" in title.text:
                outInfo += title.text.strip()+"\n"
                outInfo += "https://www.ptt.cc" + title.find("a")['href']+"\n"

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
