#導入 Discord.py
import discord
import os

#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #如果包含 ping，機器人回傳 pong
    if message.content == 'ping':
        await message.channel.send('pong')

client.run(os.environ['DISCORD_ACCESS_TOKEN']) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面