from chapter_update import update
from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin
from database import sql_start
from adding_and_processing_queue import query_processing
import aioschedule as schedule
import asyncio
client.register_handlers_client(dp)


async def scheduler():
    schedule.every(10).seconds.do(query_processing)
    schedule.every(30).minutes.do(update)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    sql_start.sql_start()
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
