from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State , StatesGroup
from help_bot import dp, bot
from aiogram import types, Dispatcher
from sql import data , user_data

class admin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    article = State()

# Команды
async def help_admins(message:types.Message):
    
    people = await data.check_admin(message.from_user.id)
    
    if len(people) != 0:
        await message.reply('Комманды: \n/add_admins \n/new_shoes \n/delet_product (артикул товара)')

# Добавление админов
async def all_admins_add(message:types.Message):
    
    people = await data.check_admin(message.from_user.id)
    chat = '-620322574'
    
    if len(people) != 0 :
        try:
            
            member = await bot.get_chat_administrators(chat)
    
            for admins in member:
                
                userId = admins.user.id
                admin_in_db = await data.check_admin(userId)
                
                if admin_in_db is None:
                    await data.add_admin(userId)
                
                else:
                    continue

            await message.reply('Всё прошло успешно') 
    
        except SyntaxError as e:
            print('Error', e)
    
    else:
        await message.reply('У вас недостаточно прав')

# Добавление ботинок
async def start_add(message:types.Message):
    
    people = await data.check_admin(message.from_user.id)
    
    if len(people) != 0:
        await admin.photo.set()
        await message.reply('Отправьте фото')
    
    else:
        await message.reply('У вас недостаточно прав')

# Первый шаг
async def photo_add(message:types.Message, state: FSMContext):
    
    people = await data.check_admin(message.from_user.id)
    
    if len(people) != 0:
        async with state.proxy() as date:
            date['photo'] = message.photo[0].file_id
    
        await admin.next()
        await message.reply('Введите имя обуви')

# Второй шаг
async def name_add(message: types.Message, state: FSMContext):
    
    people = await data.check_admin(message.from_user.id)
    
    if len(people) != 0:

        async with state.proxy() as date :
            date['name'] = message.text
    
        await admin.next()
        await message.reply('Введите описание продукта')

# Третий шаг
async def desc_add(message: types.Message , state: FSMContext):
    
    people = await data.check_admin(message.from_user.id)
    
    if len(people) != 0:

        async with state.proxy() as date:
            date['description'] = message.text
        
        await admin.next()
        await message.reply('Введите цену')

# Четвертый шаг
async def price_add(message: types.Message, state: FSMContext):
    
    people = await data.check_admin(message.from_user.id)
    
    if len(people) != 0:
        async with state.proxy() as date:
            date['price'] = int(message.text)
        
        await admin.next()
        await message.reply('Введите артикул')

# Финиш
async def article_add(message:types.Message, state:FSMContext):
    
    people = await data.check_admin(message.from_user.id)
    
    if len(people) != 0:
        async with state.proxy() as date :
            date['article'] = int(message.text)
    
        try:
            await data.add_product(state)
            await message.reply('Все успешно добавлено')
    
        except SyntaxError as e:
            await message.reply('Что то пошло не так!')
            print('Error',e)
    
        finally:
            await state.finish()

# Удаление ботинок с помощью артикула
async def delet(message: types.Message):
    
    people = await data.check_admin(message.from_user.id)
    
    if people is None: 
        await message.reply('У вас недостаточно прав!!!')
    
    else:
        
        e = message.text
        world_list = e.split()
        value = []

        for word in world_list:
            if word.isnumeric():
                value.append(int(word))
        
        if len(value) != 0:
            for i in value:
                await data.delete_in_db(i)
            
            await message.reply('Всё успешно удалено')


async def check_users(message: types.Message):
    check_admin = message.from_user.id
    
    if str(check_admin) != '1509710563':
        await message.reple('У вас нет прав!')

    else:
        people = await user_data.check_all_user()
        for r in people:
            await bot.send_message(message.from_user.id,f'id_user:{r[1]} \nИмя:{r[2]} \nАдресс:{r[3]} \nТелефон:{r[4]}')

def register_admin(dp:Dispatcher):

    dp.register_message_handler(help_admins, commands=['help_admin'])
    
    dp.register_message_handler(all_admins_add, commands=['add_admins'])

    dp.register_message_handler(start_add, commands=['new_shoes'], state=None)
    
    dp.register_message_handler(photo_add ,content_types=['photo'], state=admin.photo)
    
    dp.register_message_handler(name_add, state=admin.name)

    dp.register_message_handler(desc_add,state=admin.description)
    
    dp.register_message_handler(price_add,state=admin.price)
    
    dp.register_message_handler(article_add, state=admin.article)

    dp.register_message_handler(delet, commands=['delet_product']) 

    dp.register_message_handler(check_users, commands=['all_people'])