import telebot
from telebot import types

bot = telebot.TeleBot('6127157367:AAFgUdLVGivCz0TlO9J-5NtcdXun3AvilBs')

user_state = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id

    user_state[user_id] = 'waiting_info'

    bot.reply_to(message, "Привет! Это бот для регистрации на день физтеха!\n Введите ваше ФИО и группу:")


@bot.message_handler(func=lambda message: user_state.get(message.from_user.id) == 'waiting_info')
def handle_text(message):
    user_id = message.from_user.id
    user_info = message.text

    with open(f'user_info_{user_id}.txt', 'w') as file:
        file.write(f'Информация от пользователя {user_id}:\n')
        file.write(f'{user_info}\n')

    user_state[user_id] = 'waiting_choice'

    options = ['ИРИТ', 'ИТС', 'ИЯЭиТФ', 'ИНЭЛ', 'ИФХТиМ', 'ИПТМ', 'ИНЭУ', 'АВШ']
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(*options)
    bot.reply_to(message, "Выберите Ваш институт", reply_markup=reply_markup)

    user_state[user_id] = 'waiting_choice_1'


@bot.message_handler(
    func=lambda message: user_state.get(message.from_user.id) == 'waiting_choice_1' and message.text in ['ИРИТ', 'ИТС',
                                                                                                         'ИЯЭиТФ',
                                                                                                         'ИНЭЛ',
                                                                                                         'ИФХТиМ',
                                                                                                         'ИПТМ', 'ИНЭУ',
                                                                                                         'АВШ'])
def handle_choice_1(message):
    user_id = message.from_user.id
    user_choice = message.text

    with open(f'user_info_{user_id}.txt', 'a') as file:
        file.write(f'Ответ на первый вопрос: {user_choice}\n')

    user_state[user_id] = 'waiting_choice_2'

    options = ['Команда № 1', 'Команда № 2', 'Команда № 3', 'Команда № 4', 'Команда № 5', 'Команда № 6', ]
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(*options)
    bot.reply_to(message, "Выберите один из вариантов для второго вопроса:", reply_markup=reply_markup)


@bot.message_handler(
    func=lambda message: user_state.get(message.from_user.id) == 'waiting_choice_2' and message.text in ['Команда № 1',
                                                                                                         'Команда № 2',
                                                                                                         'Команда № 3',
                                                                                                         'Команда № 4',
                                                                                                         'Команда № 5',
                                                                                                         'Команда № 6', ])
def handle_choice_2(message):
    user_id = message.from_user.id
    user_choice = message.text

    with open(f'user_info_{user_id}.txt', 'a') as file:
        file.write(f'Ответ на второй вопрос: {user_choice}\n')

    user_state.pop(user_id)

    bot.reply_to(message, "Спасибо! Ваши ответы записаны.", reply_markup=types.ReplyKeyboardRemove())


bot.polling()
