# 在https://my.telegram.org/中获取api，并将以下信息替换为你自己的 API 密钥和相关配置
# 先在本地跑通，获取chat_name.session，再扔上github
api_id = 12345
api_hash = 'hash'

CHANNEL_ID = '@channel_id'

import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon import events
import sys

# 定义处理返回消息的回调函数
async def handle_message(event):
    message = event.message

    # 查找 "账户" 按钮并点击
    if hasattr(message, 'reply_markup') and hasattr(message.reply_markup, 'rows'):
        for row in message.reply_markup.rows:
            for button in row.buttons:
                if button.text == '账户':
                    await event.client(GetBotCallbackAnswerRequest(
                        CHANNEL_ID,
                        message.id,
                        data=button.data
                    ))
                    break

    # 查找 "每日签到" 按钮并点击
    if hasattr(message, 'reply_markup') and hasattr(message.reply_markup, 'rows'):
        for row in message.reply_markup.rows:
            for button in row.buttons:
                if button.text == '每日签到':
                    await event.client(GetBotCallbackAnswerRequest(
                        CHANNEL_ID,
                        message.id,
                        data=button.data
                    ))
                    event.client.remove_event_handler(handle_message)
                    sys.exit(0)
                    break

async def main():
    async with TelegramClient('chat_name', api_id, api_hash) as client:

        # 发送 '/reset' 到频道
        await client.send_message(CHANNEL_ID, '/reset')

        # 获取对话实体
        entity = await client.get_entity(CHANNEL_ID)

        # 添加事件处理程序来处理返回消息
        client.add_event_handler(handle_message, events.NewMessage(incoming=True, chats=[entity]))

        # 开始监听事件并等待操作完成
        await client.run_until_disconnected()

# 运行主程序
try:
    asyncio.run(main())
except SystemExit as e:
    print('finished')
    pass