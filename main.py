from aiogram import executor, types
from help_bot import dp
from handlers import user , admin
from sql import data , user_data

async def start(_):
    print('Бот вошёл в сеть')
    await data.start()
    await user_data.start()

admin.register_admin(dp)
user.register_user(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start)