import telebot
from covid import Covid
from telebot import types

bot = telebot.TeleBot("1145217564:AAHAg4iqqEyxto-VweYxtYXMrLNhkjqWW7Y")
covid = Covid()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    btn1 = types.KeyboardButton("Во всем мире")
    btn2 = types.KeyboardButton("Россия")
    btn3 = types.KeyboardButton("Украина")
    btn4 = types.KeyboardButton("США")
    markup.add(btn1, btn2, btn3, btn4)

    send_mess = f"<b>Привет {message.from_user.first_name}!</b>\nВыберите страну"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "сша":
        location = covid.get_status_by_country_name("us")
    elif get_message_bot == "украина":
        location = covid.get_status_by_country_name("ukraine")
    elif get_message_bot == "россия":
        location = covid.get_status_by_country_name("russia")
    else:
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()
        final_message = f"<u>Данные по всему миру:</u>\n<b>Заболевших: </b>{confirmed}\n" \
                        f"<b>Смертей: </b>{deaths}\n<b>Выздоровлений: </b>{recovered}"

    if final_message == "":
        final_message = f"<u>Данные в {get_message_bot}:</u>\n<b>Заболевших: </b>{location['confirmed']}\n" \
                        f"<b>Смертей: </b>{location['deaths']}\n<b>Выздоровлений: </b>{location['recovered']}"

    bot.send_message(message.chat.id, final_message, parse_mode='html')


bot.polling(none_stop=True)