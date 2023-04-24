from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram import F
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup)
import requests
import datetime

API_TOKEN: str = '<your_token_bot>'

bot: Bot = Bot(token = API_TOKEN)
dp: Dispatcher = Dispatcher()
users: dict = {}


def new_user(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'groupIdSelected': None,
                                       'groupId': 0}
    return True


# /start
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ бот-помощник, могу напомнить тебе расписание в Самарском университете')
    await message.answer_sticker(sticker = "CAACAgIAAxkBAAEH-SZkAcQXIsWzygeKBDuHIGXQv1iNvAAC3gIAAkKxQgMZO3f3XXUG6C4E")
    if message.from_user.id not in users:
        users[message.from_user.id] = {'groupIdSelected': None,
                                       'groupId': 0}


# /author
async def process_author_command(message: Message):
    await message.answer('Это автор: https://t.me/Hundestahl')


# /help
async def process_help_command(message: Message):
    await message.answer('Выбери свою группу с помощью команды /select и я отправлю расписание после команды /schedule')

button_1: KeyboardButton = KeyboardButton(text='6131-090401D')
button_2: KeyboardButton = KeyboardButton(text='6132-090401D')
button_3: KeyboardButton = KeyboardButton(text='6133-090401D')

keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1, button_2, button_3]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

# /select
async def process_select_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'groupIdSelected': None,
                                       'groupId': 0}
    await message.answer("Выбери нужную группу:\nЕсли твоей группы нет в списке, напиши автору бота", reply_markup = keyboard)


@dp.message(Text(text='6131-090401D'))
async def process_first_answer(message: Message):
    users[message.from_user.id] = {'groupIdSelected': True,
                                       'groupId': 755933208}
    await message.answer("Отлично, группа выбрана,\nжми /schedule")
@dp.message(Text(text='6132-090401D'))
async def process_second_answer(message: Message):
    users[message.from_user.id] = {'groupIdSelected': True,
                                    'groupId': 755933209}
    await message.answer("Отлично, группа выбрана,\nжми /schedule")
@dp.message(Text(text='6133-090401D'))
async def process_third_answer(message: Message):
    users[message.from_user.id] = {'groupIdSelected': True,
                                    'groupId': 755933211}
    await message.answer("Отлично, группа выбрана,\nжми /schedule")


# /schedule
async def process_sсhedule_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'groupIdSelected': None,
                                       'groupId': 0}
    if users[message.from_user.id]['groupId'] == 0:
        await message.answer("Сначала выбери нужную группу:", reply_markup = keyboard)
        return True

    current_dt = datetime.datetime.now() # Сегодняшняя дата
    it_day = current_dt.strftime('%w')
    url = "https://ssau.ru/rasp?groupId=" + str(users[message.from_user.id]['groupId']) + "&selectedWeekday=" + str(it_day) # + номер дня недели
    page = requests.get(url)
    data = page.text
    bs4 = BeautifulSoup(data, 'html.parser')
    currDay = current_dt.strftime('%d.%m.%y')
    await message.answer("Сегодня " + currDay + ", как обычно трудный день")

    subject = []
    for tag in bs4.find_all("div", 'schedule__item schedule__item_show'):
        subject.append("{}".format(tag.text))
    lesson_time = []
    for tag in bs4.find_all("div", 'schedule__time'):
        lesson_time.append("{}".format(tag.text))
    schedule = []
    for i in range(len(lesson_time)):
        if subject[i] == "":
            schedule.append(lesson_time[i] + "Здесь ничего")
        else:
            schedule.append(lesson_time[i] + subject[i])

    answer = ""
    for i in range(len(schedule)):
        answer = answer + schedule[i] + "\n"
    await message.answer(answer)


dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(process_author_command, Command(commands=['author']))
dp.message.register(process_sсhedule_command, Command(commands=['schedule']))
dp.message.register(process_select_command, Command(commands=['select']))


if __name__ == '__main__':
    dp.run_polling(bot)
