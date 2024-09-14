from flask import Flask, request, abort
import os
from service.Clawer import returnTextMessage,getBeautyUrl

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
app = Flask(__name__)

# Channel Access Token
configuration = Configuration(access_token=os.environ['LINE_ACCESS_TOKEN'])
# Channel Secret
handler = WebhookHandler(os.environ['LINE_SECRET'])

# 監聽所有來自 /callback 的 Post Request
@app.route('/callback', methods=['POST'])
def callback():

    print('callback 1')
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    print('on Call' + event.message.text)

    if '!妹子' in event.message.text:
        imageUrl = getBeautyUrl()
        print('imageUrl' + imageUrl)
        if imageUrl != '':
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[ImageMessage(text=imageUrl)]
                    )
                )

    else:
        outInfo = returnTextMessage(event.message.text)

        if outInfo != '':
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=outInfo)]
                    )
                )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
