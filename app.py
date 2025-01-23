import asyncio
import schedule
from datetime import datetime
from telegram import Bot, ChatPermissions
import apis

BOT_TOKEN = apis.TELEGRAM_BOT_TOKEN_API
GROUP_CHAT_ID = apis.TELEGRAN_REPORT_GROUP_API
bot = Bot(token = BOT_TOKEN)

allow_messages = ChatPermissions(can_send_messages=True)
restrict_messages = ChatPermissions(can_send_messages=False)

async def enable_text_messages():
    try:
        await bot.set_chat_permissions(chat_id=GROUP_CHAT_ID, permissions = allow_messages)
        print(f"[{datetime.now()}] Enabled text messages for members.")
    except Exception as e:
        print(f"Error enabling messages: {e}")

async def disable_text_messages():
    try:
        await bot.set_chat_permissions(chat_id=GROUP_CHAT_ID, permissions=restrict_messages)
        print(f"[{datetime.now()}] Disabled text messages for members.")
    except Exception as e:
        print(f"Error disabling messages: {e}")

def schedule_task(coro):
    asyncio.create_task(coro)

schedule.every().day.at("19:00").do(schedule_task, enable_text_messages())
schedule.every().day.at("19:45").do(schedule_task, disable_text_messages())

async def main_loop():
    print("Bot is running...")
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except RuntimeError as e:
        print(f"Error: {e}.")
