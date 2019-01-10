from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests
import random

import json

host='http://api.thingspeak.com'
read_api_key='EEJVY94NPX366TX3'
channel_id='618532'
url='%s/channels/%s/feeds/last.json?api_key=%s' \
     %(host, channel_id, read_api_key)
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Ol5cQvtsoujHtK58E93N1T7EefZyntOhUv2UZAdlpG47nNRXJkkGTfF8DpDMfs3nbyCJyKgxSBciQe7zn3bYqUAg/5KfV+orLnUQz+QSJBM2n8xwtn4UYhluwN3yXt7AuP1VGQ0Whc+siQHg4wbIawdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('08c5f664bbbd7d5f0435a2de312d97fe')

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
def handle_message(event):
    tokens = event.message.text.split()
    ans = ""
    if tokens[0] == "指令":
        ans = "輸入「飯」將骰出飯類店家\n"
        ans = ans + "輸入「麵」將骰出麵類店家\n"
        ans = ans + "輸入「加入 飯/麵 店家名」將登錄店家到飯或麵類"
    elif tokens[0] == "飯":
        data = requests.get('http://140.120.182.119/final/search.php?tableName=rice')
        data = json.loads(data.text)
        random.shuffle(data)
        for i in range(2):
            ans = ans + data[i][1] + "\n"
        ans = ans + "http://140.120.182.119/final/indexShowAddress.html?tableName=rice&id1="+data[0][0]+"&id2="+data[1][0]
    elif tokens[0] == "麵":
        data = requests.get('http://140.120.182.119/final/search.php?tableName=noodles')
        data = json.loads(data.text)
        random.shuffle(data)
        for i in range(2):
            ans = ans + data[i][1] + "\n"
        ans = ans + "http://140.120.182.119/final/indexShowAddress.html?tableName=noodles&id1="+data[0][0]+"&id2="+data[1][0]
    elif tokens[0] == "加入":
        sql = ""
        if len(tokens) < 2:
            ans = "指令無效，加入店家失敗"
        elif tokens[1] == "飯":
            sql = "http://140.120.182.119/final/insert.php?tableName=rice"
        elif tokens[1] == "麵":
            sql = "http://140.120.182.119/final/insert.php?tableName=noodles"
        else:
            ans = "指令無效，加入店家失敗"

        if len(tokens) < 3:
            ans = "指令無效，加入店家失敗"
        else:
            sql = sql + "&Name=" + tokens[2]
        if ans == "":
            data = requests.get(sql)
            data = data.text
            if data == "1":
                ans = "加入店家成功"
            else:
                ans = "加入店家失敗"
    else:
        ans = "無此指令，可以輸入「指令」查詢可用指令"
    message = TextSendMessage(text=ans)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)