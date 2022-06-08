import telebot
import sqlite3
#Токен и создание переменной бота
bot = telebot.TeleBot('5305291753:AAFnf63hT4afETcoJFGY1js7uDRYjMvHXSY')

######################################################################################
#
#   ver: 1.0.0
#   Ready and work:
#   Создание заданий, игроков, логика игры
#
#       ||             ||
#       ||             ||
#       ||             ||
#
#
#       \              /
#        \____________/
#
#                                                                 My links:
#                                                       https://t.me/milliondollaruser
#                                                             https://t.me/noofme
######################################################################################

#Создание клавиатур
keyboardstart = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardstart.row('Играть', 'Помощь')

keyboardhelp = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardhelp.row('Связаться с админом', 'Назад')

keyboardadmin = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardadmin.row('Играть', 'Добавить задания', 'Удалить задания')

keyboardstarty = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardstarty.row('Начать', 'Назад')

keyboardnext = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardnext.row('Следующее задание', 'Назад')

#Подключение БД для имен игроков
db = sqlite3.connect('server.db', check_same_thread=False)
curs = db.cursor()
curs.execute("""CREATE TABLE IF NOT EXISTS users (
	createdname TEXT
)""")
db.commit()
print('DB sevrer created/found')
#Подключение БД для заданий
database = sqlite3.connect('roulete.db', check_same_thread=False)
c = database.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS zadaniya (
    zadaniye TEXT
)""")
database.commit()
print('DB roulete created/found')
#Тут ID пользователя ТГ, кто будет админом и сможет добавлять задания.
admin_id = 499301842 #5064936782

#Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    curs.execute("DELETE FROM users")
    if message.from_user.id == admin_id:
        bot.send_message(message.chat.id, 'Добро пожаловать в админ панель!', reply_markup=keyboardadmin)
    else:
        bot.send_message(message.chat.id, 'Добро пожаловать в игру "Правда или действие"', reply_markup=keyboardstart)

#Обработчик любых текстовых сообщений и клавиатур
@bot.message_handler(content_types=['text'])
def send_message(message):
    global usv

    if message.text == 'Следующее задание':
            #Обращаемся к БД и рандомим имя и задание
            for value in curs.execute("SELECT * FROM `users` ORDER BY RANDOM() LIMIT 1"):
                bot.send_message(message.chat.id, f'Задание для игрока "{value[0]}":')
            for value in c.execute("SELECT * FROM `zadaniya` ORDER BY RANDOM() LIMIT 1"):
                bot.send_message(message.chat.id, f'{value[0]}', reply_markup=keyboardnext)

    if message.text == 'Удалить задания':
        bot.send_message(message.chat.id, 'Введи задание, которое хочешь удалить:')

        for value in c.execute("SELECT * FROM `zadaniya`"):
            bot.send_message(message.chat.id, f'{value[0]}')

        bot.register_next_step_handler(message, delete)

    if message.text == 'Начать':
        bot.send_message(message.chat.id, 'Начало игры!', reply_markup=keyboardnext)
    if message.text == 'Играть':
        bot.send_message(message.chat.id, 'Сколько будет игроков?:')
        bot.register_next_step_handler(message, pp)
    if message.text == 'Список':
        bot.send_message(message.chat.id, 'Список игроков:')
        sendusers(message)
    if message.text == 'Помощь':
        bot.send_message(message.chat.id, '🎲Правила очень простые :\n'
                                          '📌Играют от 4 до 10 чел\n'
                                          '📌Выпивает тот, кому скажет карточка. Выполнил задание - нажал кнопку "Дальше"\n'
                                          '📌Сколько пить - скажет карточка\n'
                                          '📌Все движения по кругу осуществляются по часовой стрелке\n'
                                          '🤩Наливай "прохладительные" напитки, усаживайся поудобнее и выполняй все задания. Твою компанию ждет угарная и необычная вечеринка\n'
                                          '👆Клик "Играть" если готовы играть.\n'
                                          'Чтобы начать игру заново отправь /start в чат.', reply_markup=keyboardhelp)
    if message.text == 'Связаться с админом':
        bot.send_message(message.chat.id, 'https://t.me/nccccccrnnn', reply_markup=keyboardhelp)
    if message.text == 'Назад':
        if message.from_user.id == admin_id:
            bot.send_message(message.chat.id, 'Главное меню', reply_markup=keyboardadmin)
        else:
            bot.send_message(message.chat.id, 'Главное меню', reply_markup=keyboardstart)
    if message.text == 'Добавить задания':
        bot.send_message(message.chat.id, 'Введи новое задание:')
        bot.register_next_step_handler(message, new)

def delete(message):
    bot.send_message(message.chat.id, f'Удалим {message.text}')
    c.execute(f"DELETE FROM zadaniya WHERE zadaniye = '{message.text}'")
    database.commit()


    bot.send_message(message.chat.id, 'Обновленный список заданий:')
    for value in c.execute("SELECT * FROM `zadaniya`"):
        bot.send_message(message.chat.id, f'{value[0]}', reply_markup=keyboardadmin)
#Обработчик создания новых заданий
def new(message):
    c.execute(f"SELECT zadaniye FROM zadaniya WHERE zadaniye = '{message.text}'")
    if c.fetchone() is None:
        c.execute(f"INSERT INTO zadaniya VALUES ('{message.text}')")
    database.commit()
    bot.send_message(message.chat.id, 'Задание добавлено.', reply_markup=keyboardadmin)
gg = 0
usv = 0
#Получение списка заданных имен
def sendusers(message):
    for value in curs.execute("SELECT createdname FROM users"):
        bot.send_message(message.chat.id, f'{str(value[0])}', reply_markup=keyboardstart)
#Создание первого игрока и задание количества игроков
def pp(message):
    global gg
    gg = int(message.text)
    bot.send_message(message.chat.id, 'Введите имя игрока:')
    bot.register_next_step_handler(message, players)
#Создание новых игроков по количеству игроков из обработки выше
def players(message):
    global usv
    nick = message.text
    if usv < gg:
        curs.execute(f"SELECT createdname FROM users WHERE createdname = '{nick}'")
        if curs.fetchone() is None:
            curs.execute(f"INSERT INTO users VALUES ('{nick}')")
            db.commit()
            print('added')
        bot.send_message(message.chat.id, f'Игроку №{usv+1}, присвоен ник {nick}')
        bot.send_message(message.chat.id, 'Введите имя следующего игрока:')
        usv+=1
        bot.register_next_step_handler(message, players)
    else:
        bot.send_message(message.chat.id, 'Игроки зарегестрированы.', reply_markup=keyboardstarty)

bot.polling() #Запуск бота
