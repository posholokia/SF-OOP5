import telebot
from config import TOKEN, keys
from extensions import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):  # выводим список доступных валют по команде
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['start', 'help'])  # как пользоваться ботом
def help(message: telebot.types.Message):
    text = 'Для получения стоимости валюты напишите мне сообщение в формате: \n<Конвертируемая валюта>' \
           '<В какую валюту нужно конвертировать> <Количество валюты> ' \
           '\nСписок доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  # принимаем команду для конвертации
def convert(message: telebot.types.Message):
    values = message.text.lower().split(' ')  # помещаем команду пользователя в список
    try:  # проверяем, что введено достаточно параметров команды и их можно обработать
        if len(values) > 3:
            raise APIException(f'Вы указали слишком много параметров: {str(*values[3:])}')
        elif len(values) < 3:
            raise APIException(f'Вы указали недостаточно параметров')
        # объявляем переменные из команды пользователя - конвертируемая валюта, во что конвертируем и кол-во
        quote, base, amount = values
        rate = ExchangeCurrency.get_price(quote, base, amount)  # получаем курс конвертации
    except APIException as e:  # ловим пользовательские ошибки
        bot.reply_to(message, f'{e}\nЧтобы посмотреть как меня использовать наберите /help'
                              f'\nСписок доступных валют: /values')
    except Exception as e:  # ловим серверные ошибки
        bot.reply_to(message, f'Что-то пошло не так ¯\_(ツ)_/¯\n{e}')
    else:
        convert = round(rate * int(amount), 4)  # значение конвертируемой валюты, 4 знака после запятой
        bot.send_message(message.chat.id, f'{amount} {quote} - {convert} {base}')


bot.polling(none_stop=True)

