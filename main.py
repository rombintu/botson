import telebot

from telebot import types
from config import TOKEN

from func import convert_rub, check_int
import dbfunc as db

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text', 'document'])
def getMessage(message):
    id_user = message.from_user.id
    text = message.text

    commands = ['Добавить цель', 'Мои цели','Накопления']
    keyboard = types.ReplyKeyboardMarkup()
    
    def printb(mess):
        bot.send_message(id_user, mess)

    if text == '/start':
        smile_start = b'\xF0\x9F\x98\xBC'.decode()
        keyboard.row(commands[0], commands[1])
        keyboard.row(commands[2])
        bot.send_message(id_user, f"Привет, я бот, я помогу тебе с финансами {smile_start}", reply_markup=keyboard)
    elif text == '/convert': # Конвертер
        def convert(message):
            text = message.text
            if check_int(text):
                summa = int(text)
                smile_dollar = b'\xF0\x9F\x92\xB2'.decode()
                smile_euro = b'\xF0\x9F\x92\xB6'.decode()
                usd, eur, s = convert_rub(summa)
                buff = f"Доллар: {usd}₽ {smile_dollar}\nЕвро: {eur}₽ {smile_euro}\nСумма в $: {s[0]}\nСумма в €: {s[1]}"
                printb(buff)
            else:
                printb('Сумма должна быть числом, отмена операции')

        printb("Введи сумму в рублях")
        bot.register_next_step_handler(message, convert)
    elif text == commands[0]: # Добавить цель
        new_target = []

        def add_target_title(message):
            title = message.text
            new_target.append(title)
            printb("Введи сумму в рублях")
            bot.register_next_step_handler(message, add_target_cost)

        def add_target_cost(message):
            text = message.text
            if check_int(text):
                new_target.append(int(text))
                db.add_target((new_target[0], new_target[1]))
                printb('Готово, цель добавлена')
            else:
                printb('Сумма должна быть числом, отмена операции')
            
        printb("Введи название цели")
        bot.register_next_step_handler(message, add_target_title)

    elif text == commands[1]:
        targets = db.select_target()
        buff = ''
        for i, target in enumerate(targets):
            buff += f'{i+1}. {target[1]} : {target[2]}₽\n'

        printb(f"Мои цели: \n{buff}")
        
    else:
        smile_end = b'\xF0\x9F\x98\xBF'.decode()
        keyboard.row(commands[0], commands[1])
        keyboard.row(commands[2])
        bot.send_message(id_user, f"Извини, я не знаю такой команды {smile_end}", reply_markup=keyboard)


if __name__ == "__main__":
    print('Bot active')
    bot.polling(none_stop=True)