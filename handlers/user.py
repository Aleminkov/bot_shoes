from aiogram import types
from help_bot import bot, Dispatcher
from sql import data , user_data
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State , StatesGroup

#Приветстветие
async def welcome(message: types.Message):
    people = await user_data.check_user(message.from_user.id)
    
    if people is None:
        await user_data.new_user(message.from_user.id)
    
    await bot.send_message(message.from_user.id,f'Hello! This is shoes bot . My creator is Aleminkov. Commands: /menu, /phone, /adress, /buy(vendor code), /registor')

#Регистрация
class Registor(StatesGroup):
    name = State()
    adress = State()
    phone = State()

async def reg(message: types.Message):
    
    await Registor.name.set()
    await message.reply('Напишите свое имя.')

async def name_add(message:types.Message, state:FSMContext):
    async with state.proxy() as date :
        date['name'] = message.text

    await Registor.next()
    await message.reply('Напишите адресс(можете не писать кв)')

async def adress_add(message:types.Message, state:FSMContext):
        
    try:
        async with state.proxy() as date :
            date['address'] = message.text

        await Registor.next()
        await message.reply('Напишите номер телефона(объязательно!)')
    
    except SyntaxError as e:
        await message.reply('Что то пошло не так!')
        print('Error',e)

async def phone_add(message: types.Message, state:FSMContext):
        
    try:
        async with state.proxy() as date :
            date['phone'] = message.text

        await user_data.registor(state,message.from_user.id)
        await message.reply('Всё успешно добавлено!')
    
    except SyntaxError as e:
        await message.reply('Что то пошло не так!')
        print('Error',e)
    
    finally:
        await state.finish()

#Меню
async def menu(message: types.Message):
    product = await data.read_sql()

    for r in product:
        await bot.send_photo(message.from_user.id, r[1], f'Название: {r[2]}\nОписание: {r[3]}\nЦена: {r[4]}\nАртикул: {r[5]}')

#Отправка номера телефона
async def phone(message: types.Message):
    await bot.send_message(message.from_user.id, '+79002159802')

#Регистратор команд
def register_user(dp: Dispatcher):

    dp.register_message_handler(welcome, commands=['start', 'help'])

    dp.register_message_handler(menu, commands=['menu'])

    dp.register_message_handler(phone, commands=['phone'])

    dp.register_message_handler(reg,commands=['registor'])
    
    dp.register_message_handler(name_add,state=Registor.name)

    dp.register_message_handler(adress_add,state=Registor.adress)

    dp.register_message_handler(phone_add,state=Registor.phone)