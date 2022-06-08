import telebot
import sqlite3
import uuid

######################################################################################
#
#   ver: 1.0.3
#   Ready and work:
#   ban/unban, promo, give cash/take cash, give admin, link nickname
#
#       ||             ||
#       ||             ||
#       ||             ||
#
#
#       \              /
#        \____________/
#
#
#   TODO: Games, games counter, statistics, games amount, admins
#                                                                   https://t.me/noofme
######################################################################################




bot = telebot.TeleBot('5337208574:AAFfv0KdSS3tz1h3iSvm5umhvpYDQWx6Wx0')


team = telebot.types.InlineKeyboardMarkup()
minimenu = telebot.types.InlineKeyboardMarkup()
gamesmenu = telebot.types.InlineKeyboardMarkup()
matches1 = telebot.types.InlineKeyboardMarkup()
matches2 = telebot.types.InlineKeyboardMarkup()
matches3 = telebot.types.InlineKeyboardMarkup()
matchesbash = telebot.types.InlineKeyboardMarkup()
cabmenu = telebot.types.InlineKeyboardMarkup()
offermenu = telebot.types.InlineKeyboardMarkup()
understand = telebot.types.InlineKeyboardMarkup()
adminmenu = telebot.types.InlineKeyboardMarkup()
matchesmenu = telebot.types.InlineKeyboardMarkup()
mmenu = telebot.types.InlineKeyboardMarkup()
gameplay = telebot.types.InlineKeyboardMarkup()
admin_ids = []
admin_ids.append(5064936782)
promo = []
promos = []
promo_num = 0

balance = 0
balance_to_give = 0
balance_to_take = 0

to = 0
the = ''
bet = 0

code = ''

bannedmenu = telebot.types.ReplyKeyboardMarkup(True, True)
bannedmenu.row('Написать админу')
bbackmenu = telebot.types.InlineKeyboardMarkup()
maps = telebot.types.InlineKeyboardMarkup()
maps.add(telebot.types.InlineKeyboardButton(text='🌵Map Maker', callback_data='maker'))
maps.add(telebot.types.InlineKeyboardButton(text='🌾Canyon Rivers', callback_data='river'))
maps.add(telebot.types.InlineKeyboardButton(text='🌑Flying Fantasies', callback_data='fly'))


menu = telebot.types.ReplyKeyboardMarkup(True, True)
menu.row('Меню')
menu.row('CHAT AND CHANNEL')
#KEYBOARDS
understand.add(telebot.types.InlineKeyboardButton(text='❌ Понятно', callback_data='unders'))

adminmenu.add(telebot.types.InlineKeyboardButton(text='Выдать права', callback_data='give'))
adminmenu.add(telebot.types.InlineKeyboardButton(text='Отозвать права', callback_data='take'))
adminmenu.add(telebot.types.InlineKeyboardButton(text='Выдать баланс', callback_data='give_money'))
adminmenu.add(telebot.types.InlineKeyboardButton(text='Отозвать баланс', callback_data='take_money'))
adminmenu.add(telebot.types.InlineKeyboardButton(text='Промокоды', callback_data='promo'))
adminmenu.add(telebot.types.InlineKeyboardButton(text='Выводы', callback_data='outcash'))
adminmenu.add(telebot.types.InlineKeyboardButton(text='Заблокировать юзера', callback_data='blacklist'))
adminmenu.add(telebot.types.InlineKeyboardButton(text='Разблокировать юзера', callback_data='whitelist'))
adminmenu.add(telebot.types.InlineKeyboardButton(text='Матчи', callback_data='mat'))

team.add(telebot.types.InlineKeyboardButton(text='🔵', callback_data='blue'))
team.add(telebot.types.InlineKeyboardButton(text='🔴', callback_data='red'))

game = telebot.types.InlineKeyboardButton('🕹ИГРЫ', callback_data='games')
sec = telebot.types.InlineKeyboardButton(text='🖥 Кабинет', callback_data='cabin')
thir = telebot.types.InlineKeyboardButton(text=' 🌐 Информация', callback_data='info')
fo = telebot.types.InlineKeyboardButton(text='👤 Админ', callback_data='admin')

minimenu.row(game)
minimenu.row(sec, thir)
minimenu.row(fo)

gamesmenu.add(telebot.types.InlineKeyboardButton(text='Столкновение', callback_data='idk'))
gamesmenu.add(telebot.types.InlineKeyboardButton(text='1 VS 1', callback_data='1v1'))
gamesmenu.add(telebot.types.InlineKeyboardButton(text='2 VS 2', callback_data='2v2'))
gamesmenu.add(telebot.types.InlineKeyboardButton(text='3 VS 3\n(ТУРНИРЫ)', callback_data='3v3'))
gamesmenu.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))


bback = telebot.types.InlineKeyboardButton(text=f'Назад', callback_data='back')
bbackmenu.row(bback)
cabmenu.add(telebot.types.InlineKeyboardButton(text='Пополнить баланс', callback_data='addmoney'))
cabmenu.add(telebot.types.InlineKeyboardButton(text='Вывести', callback_data='withdraw'))
cabmenu.add(telebot.types.InlineKeyboardButton(text='Привязать аккаунт', callback_data='linkacc'))
cabmenu.add(telebot.types.InlineKeyboardButton(text='Полная статистика', callback_data='fullstat'))
cabmenu.add(telebot.types.InlineKeyboardButton(text='Ввести промокод', callback_data='use_promo'))
cabmenu.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))

offermenu.add(telebot.types.InlineKeyboardButton(text='QIWI', callback_data='qiwi'))
offermenu.add(telebot.types.InlineKeyboardButton(text='Юмани', callback_data='umoney'))
offermenu.add(telebot.types.InlineKeyboardButton(text='FREEKASSA', callback_data='free'))
offermenu.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))

matchesmenu.add(telebot.types.InlineKeyboardButton(text='Создать матч', callback_data='create_maps'))
matchesmenu.add(telebot.types.InlineKeyboardButton(text='Запланировать матч', callback_data='plan_match'))
matchesmenu.add(telebot.types.InlineKeyboardButton(text='Запустить матч', callback_data='start_map'))

gameplay.add(telebot.types.InlineKeyboardButton(text='➕ Подключится', callback_data='connect'))
gameplay.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back_to_games'))
checklink = False

users = sqlite3.connect('users.db', check_same_thread=False)
c = users.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
usernames TEXT,
chatid BIGINT,
balance INT,
isbanned INT,
nickname TEXT,
islinked INT,
registred_to_match INT,
warns INT,
isadmin INT
)""")
c.execute("""CREATE TABLE IF NOT EXISTS matches (
mapname TEXT,
bet INT,
people INT,
peoplereg INT,
image_of_map_src TEXT,
type TEXT,
game_id INT NOT NULL PRIMARY KEY
)""")


users.commit()
print('DB users created/found')

for value in c.execute("SELECT game_id FROM 'matches' ORDER BY game_id DESC LIMIT 1"):
    i = 1
    to = int(value[0])
    while i <= to:
        for value in c.execute(f"SELECT mapname, bet, people, type, peoplereg FROM matches WHERE game_id = {i}"):
            if value[3] == '1v1':
                matches1.add(telebot.types.InlineKeyboardButton(text=f'{value[0]} | {value[1]} | {value[4]} / {value[2]}', callback_data=f'{i}'))
                i+=1
            if value[3] == '2v2':
                matches2.add(telebot.types.InlineKeyboardButton(text=f'{value[0]} | {value[1]} | {value[4]} / {value[2]}', callback_data=f'{i}'))
                i+=1
            if value[3] == '3v3':
                matches3.add(telebot.types.InlineKeyboardButton(text=f'{value[0]} | {value[1]} | {value[4]} / {value[2]}', callback_data=f'{i}'))
                i+=1
            if value[3] == 'Столкновение':
                matchesbash.add(telebot.types.InlineKeyboardButton(text=f'{value[0]} | {value[1]} | {value[4]} / {value[2]}',
                                                                callback_data=f'{i}'))
                i += 1


@bot.message_handler(commands=['warn'])
def warnuser(message):
    for value in c.execute(f"SELECT isadmin FROM users WHERE chatid = '{message.chat.id}'"):
        if value[0] == 1:
            bot.send_message(message.chat.id, 'Введите юзернейм пользователя, которому нужно выдать варн')
            bot.register_next_step_handler(message, warn2)
        else:
            bot.send_message(message.chat.id, 'Ошибка, вы не можете выдавать варны!')
def warn2(message):
    c.execute(f"UPDATE users SET warns = warns + 1 WHERE usernames = '{message.text}'")
    bot.send_message(message.chat.id, 'Варн выдан.')
    for value in c.execute(f"SELECT warns, chatid FROM users WHERE usernames = '{message.text}'"):
        if value[0] >= 5:
            c.execute(f"UPDATE users SET isbanned = 1 WHERE usernames = '{message.text}'")
        bot.send_message(value[1], f'Администратор {message.from_user.username} выдал варн. Всего варнов: {value[0]}')
    users.commit()



@bot.message_handler(commands=['start'])
def start(message):
    global username
    c.execute(f"SELECT usernames FROM users WHERE usernames = '{message.from_user.username}'")
    if c.fetchone() is None:
        c.execute(f"INSERT INTO users VALUES ('{message.from_user.username}', '{message.chat.id}', '{0}', '{0}', '?', '{0}', '{0}', '{0}', {0})")
        users.commit()
    username = message.from_user.username
    for value in c.execute(f"SELECT isadmin FROM users WHERE chatid = '{message.chat.id}'"):
        if value[0] == 1:
            bot.send_message(message.chat.id, 'Добро пожаловать в админку!', reply_markup=adminmenu)
        else:
            try:
                for value in c.execute(f"SELECT isbanned FROM users WHERE usernames = '{message.from_user.username}'"):
                    if value[0] == 1:
                        bot.send_message(message.chat.id, 'Вы заблокированы в этом боте. Вам тут не рады. ', reply_markup=bannedmenu)
                    else:
                        bot.send_message(message.chat.id, '❗️Добро пожаловать, здесь проходят  разнообразные турниры в Brawl Starts!', reply_markup=menu)
            except telebot.apihelper.ApiTelegramException:
                pass



@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text == 'CHAT AND CHANNEL':
        img = open('menuimg.PNG', 'rb')
        bot.send_photo(message.chat.id, img, caption='🔥 Это место, где ты должен быть, заходи быстрее!\n'
                                          '\n'
                                          '📢 https://t.me/Brawl_Starts_Channel\n'
                                          '💬 https://t.me/Brawl_Starts_Chat', reply_markup=understand)

        img.close()
    if message.text == 'Меню':
        imgg = open('minimenuimg.PNG', 'rb')
        bot.send_photo(message.chat.id,imgg, caption=f'👑 Добро пожаловать, {message.from_user.username}!', reply_markup=minimenu)
        imgg.close()
def forwar(message):
    c.execute(f"UPDATE users SET isadmin = 1 WHERE usernames = '{message.text}'")
    users.commit()
    for value in c.execute(f"SELECT chatid FROM users WHERE usernames = '{message.text}'"):
        bot.send_message(value[0], 'Поздравляю! Вам выданы админ права.')
    bot.send_message(message.chat.id, f'Пользователь {message.text} добавлен в админы.')
def getidbymessage(message):
    bot.send_message(message.chat.id, 'Введи юзернейм пользователя, которого ты хочешь сделать админом')
    bot.register_next_step_handler(message, forwar)
def gege(message):
    bot.send_message(message.chat.id, 'Введите сумму промокода:')
    bot.register_next_step_handler(message, givepromo)
def givepromo(message):
    promo.append(int(message.text))
    promos.append(str(uuid.uuid4()))
    bot.send_message(message.chat.id, f'Промокод: {promos[promo_num]}, на сумму {promo[promo_num]} сгенерирован.')
def use_promocode(message):
    bot.send_message(message.chat.id, 'Введите промокод:')
    bot.register_next_step_handler(message, use_promocode2)
def use_promocode2(message):
    global balance
    i = 0
    for value in promos:
        if promos[i] == message.text:
            c.execute(f"SELECT chatid FROM users WHERE usernames = '{message.chat.id}'")
            if c.fetchone() is None:
                c.execute(f"UPDATE users SET balance = balance + {promo[promo_num]} WHERE chatid = {message.chat.id}")
                users.commit()
            bot.send_message(message.chat.id, 'Промокод активирован. Средства зачислены на баланс.')
        else:
            i+=1
            value+=1
def link_acc(message):
    if c.fetchone() is None:
        c.execute(f"UPDATE users SET islinked = 1 WHERE chatid = '{message.chat.id}'")
        c.execute(f"UPDATE users SET nickname = '{message.text}' WHERE chatid = '{message.chat.id}'")
        users.commit()
    bot.send_message(message.chat.id, '✅АККАУНТ ПРИВЯЗАН', reply_markup=cabmenu)
def sendmes(message):
    if int(message.text) < 51:
        bot.send_message(message.chat.id, '❗️Сумма пополнения не должна быть меньше 50 руб')
    if int(message.text) > 51:
        bot.send_message(message.chat.id, 'Выберите способ оплаты:', reply_markup=offermenu)
def sumgive(message):
    global balance_to_give
    balance_to_give = int(message.text)
    bot.send_message(message.chat.id, 'Введите юзернейм пользователя:')
    bot.register_next_step_handler(message, sumgive2)
def sumgive2(message):
    global balance_to_give
    userid = message.text
    for value in c.execute(f"SELECT chatid FROM users WHERE usernames = '{userid}'"):
        bot.send_message(value[0], f'Выдан баланс {balance_to_give} ')
        bot.send_message(message.chat.id, 'Баланс пользователя успешно пополнен.')
        chatid = value[0]
    if c.fetchone() is None:
        c.execute(f"UPDATE users SET balance = balance + {balance_to_give} WHERE chatid = {chatid}")
        users.commit()
def sumtake(message):
    global balance_to_take
    balance_to_take = int(message.text)
    bot.send_message(message.chat.id, 'Введите юзернейм пользователя:')
    bot.register_next_step_handler(message, sumtake2)
def sumtake2(message):
    global balance_to_take
    userid = message.text
    for value in c.execute(f"SELECT chatid FROM users WHERE usernames = '{userid}'"):
        bot.send_message(value[0], f'Отозван баланс {balance_to_take} ')
        bot.send_message(message.chat.id, 'Баланс пользователя успешно отозван.')
        chatid = value[0]
    if c.fetchone() is None:
        c.execute(f"UPDATE users SET balance = balance - {balance_to_take} WHERE chatid = {chatid}")
        users.commit()
def takemoney(message):
    bot.send_message(message.chat.id, 'Введите сумму, которую хотите отозвать')
    bot.register_next_step_handler(message, sumtake)
def givemoney(message):
    bot.send_message(message.chat.id, 'Введите сумму, которую хотите выдать')
    bot.register_next_step_handler(message, sumgive)
def addtoblacklist(message):
    bot.send_message(message.chat.id, 'Введите ник игрока, которого хотите забанить:')
    bot.register_next_step_handler(message, ban)
def ban(message):
    userid = message.text
    if c.fetchone() is None:
        c.execute(f"UPDATE users SET isbanned = 1 WHERE usernames = '{userid}'")
        users.commit()
    bot.send_message(message.chat.id, f'Юзер {userid} забанен')
    for value in c.execute(f"SELECT chatid FROM users WHERE usernames = '{userid}'"):
        bot.send_message(value[0], 'Вас забанили')
def takefromblacklist(message):
    bot.send_message(message.chat.id, 'Введите ник для разбана')
    bot.register_next_step_handler(message, unban)
def unban(message):
    userid = message.text
    if c.fetchone() is None:
        c.execute(f"UPDATE users SET isbanned = 0 WHERE usernames = '{userid}'")
        users.commit()
    bot.send_message(message.chat.id, f'Юзер {userid} разбанен')
    for value in c.execute(f"SELECT chatid FROM users WHERE usernames = '{userid}'"):
        bot.send_message(value[0], 'Вас разбанили, введите /start')
def create_map(message):
    bot.send_message(message.chat.id, 'Введите название карты')
    bot.register_next_step_handler(message, create_map2)
def create_map2(message):
    global mapname
    mapname = message.text
    bot.send_message(message.chat.id, 'Введите режим(1v1, 2v2, 3v3)')
    bot.register_next_step_handler(message, create_map3)
def create_map3(message):
    global numusers, Type
    Type = message.text
    if Type == '1v1':
        numusers = 2
        bot.send_message(message.chat.id, 'Введите сумму ставки')
        bot.register_next_step_handler(message, create_map4)
    if Type == '2v2':
        numusers = 4
        bot.send_message(message.chat.id, 'Введите сумму ставки')
        bot.register_next_step_handler(message, create_map4)
    if Type == '3v3':
        numusers = 6
        bot.send_message(message.chat.id, 'Введите сумму ставки')
        bot.register_next_step_handler(message, create_map4)
    if Type == 'Столкновение':
        bot.send_message(message.chat.id, 'Введите количество игроков')
        bot.register_next_step_handler(message, bash)
def bash(message):
    global numusers
    numusers = int(message.text)
    bot.send_message(message.chat.id, 'Введите сумму ставки')
    bot.register_next_step_handler(message, create_map4)
def create_map4(message):
    global stavka
    stavka = int(message.text)
    bot.send_message(message.chat.id, 'Отправьте фото карты!')
    bot.register_next_step_handler(message, create_map_photo)
def create_map_photo(message):
    global mapname, stavka, numusers, to, Type
    try:
        bot.send_message(message.chat.id, 'Матч успешно создан.')
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            p1 = open(f'{message.document.file_name}', 'rb')
            bot.send_photo(message.chat.id, p1, caption=f'{mapname} | {stavka} | 0 / {numusers}')
        for value in c.execute("SELECT game_id FROM 'matches' ORDER BY game_id DESC LIMIT 1"):
            to = int(value[0])
        c.execute(f"INSERT INTO matches VALUES ('{mapname}', '{stavka}', '{numusers}', '{0}', '{message.document.file_name}', '{Type}', {to+1})")
        users.commit()
        if Type == 'Столкновение':
            matchesbash.add(telebot.types.InlineKeyboardButton(text=f'{mapname} | {stavka} | 0 / {numusers}',
                                                       callback_data=f'{to+1}'))
        if Type == '1v1':
            matches1.add(telebot.types.InlineKeyboardButton(text=f'{mapname} | {stavka} | 0 / {numusers}',
                                                       callback_data=f'{to+1}'))
        if Type == '2v2':
            matches2.add(telebot.types.InlineKeyboardButton(text=f'{mapname} | {stavka} | 0 / {numusers}',
                                                            callback_data=f'{to + 1}'))
        if Type == '3v3':
            matches3.add(telebot.types.InlineKeyboardButton(text=f'{mapname} | {stavka} | 0 / {numusers}',
                                                            callback_data=f'{to + 1}'))
    except AttributeError:
        bot.send_message(message.chat.id, 'Ошибка, отправьте фото как файл')
        bot.register_next_step_handler(message, create_map_photo)
def take(message):
    bot.send_message(message.chat.id, 'Введите юзернейм пользователя, у которого хотите отозвать права.')
    bot.register_next_step_handler(message, take2)
def take2(message):
    c.execute(f"UPDATE users SET isadmin = 0 WHERE usernames = '{message.text}'")
    users.commit()
    bot.send_message(message.chat.id, f'Пользователь {message.text} удален из админов.')
#maybe
def start_match1(message):
    global code
    code = message.text
    bot.send_message(message.chat.id, 'Введите ID матча, который нужно запустить:')
    bot.register_next_step_handler(message, start_match)
def start_match(message):
    global pic, mname, bbet, ppeople, Type, code
    mname = ''
    bbet = ''
    ppeople = ''
    Type = ''
    for value in c.execute(f"SELECT image_of_map_src FROM matches WHERE game_id = {int(message.text)}"):
        pic = value[0]
    for value in c.execute(f"SELECT mapname, bet, people, type FROM matches WHERE game_id = {int(message.text)}"):
        mname = value[0]
        bbet = value[1]
        ppeople = value[2]
        Type = value[3]
    for value in c.execute(f"SELECT chatid FROM users WHERE registred_to_match = {int(message.text)}"):
        bot.send_message(value[0], f'ID матча: {int(message.text)}\n'
                                   f'Код комнаты: {code}')
        bot.send_photo(value[0], photo=open(f'{pic}', 'rb'), caption=f'{mname} | {bbet} | 0 / {ppeople}\n'
                                                                            f'{Type}')
    bot.send_message(message.chat.id, f'Матч {int(message.text)} ID, запущен.')
    bot.send_photo(message.chat.id, photo=open(f'{pic}', 'rb'), caption=f'{mname} | {bbet} | 0 / {ppeople}\n'
                                                                        f'{Type}')

@bot.callback_query_handler(func=lambda call: True)
def mm(call):
    try:
        global pic, mname, bbet, ppeople, regged
        regged = 0
        mname = ''
        bbet = ''
        ppeople = ''
        print(c.fetchall())
        print(call.data)
        for value in c.execute(f"SELECT mapname, bet, people, peoplereg, image_of_map_src FROM matches WHERE game_id = {call.data}"):
            mname = value[0]
            bbet = value[1]
            ppeople = value[2]
            regged = value[3]
            pic = value[4]
        bot.send_message(call.message.chat.id, f'ID матча: {call.data}')
        bot.send_photo(call.message.chat.id, photo=open(f'{pic}', 'rb'), caption=f'{mname} | {bbet} | {regged} / {ppeople}', reply_markup=gameplay)
    except sqlite3.OperationalError:
        step(call)
def step(call):
    global checklink, username, balance, bet

    for value in c.execute("SELECT game_id FROM matches"):
        if call.data in value:
            mm(call)
    if call.data == 'back_to_games':
        bot.send_message(call.message.chat.id, 'Доступные комнаты:', reply_markup=gamesmenu)
    if call.data == 'start_map':
        bot.send_message(call.message.chat.id, 'Создайте комнату в игре и введите код для подключения к ней')
        bot.register_next_step_handler(call.message, start_match1)
    if call.data == 'take':
        take(call.message)
    if call.data == 'create_maps':
        create_map(call.message)
    if call.data == 'blue':
        c.execute(f"UPDATE users SET registred_to_match = {value[0]} WHERE chatid = '{call.message.chat.id}'")
        c.execute(f"UPDATE matches SET peoplereg = peoplereg + 1 WHERE game_id = {value[0]}")
        users.commit()
        bot.send_message(call.message.chat.id, 'Вы успешно зарегестрировались на игру за синюю команду. Ожидайте её начала.')
    if call.data == 'connect':
        bot.send_message(call.message.chat.id, 'Выберите команду:', reply_markup=team)
    if call.data == 'maker':
        pass
    if call.data == 'create_match':
        bot.send_message(call.message.chat.id, 'Выберите карту:', reply_markup=maps)
    if call.data == 'mat':
        bot.send_message(call.message.chat.id, 'Вы в меню матчей, что хотите сделать?', reply_markup=matchesmenu)
    if call.data == 'take_money':
        takemoney(call.message)
    if call.data == 'give_money':
        givemoney(call.message)
    if call.data == 'use_promo':
        use_promocode(call.message)
    if call.data == 'blacklist':
        addtoblacklist(call.message)
    if call.data == 'promo':
        gege(call.message)
    if call.data == 'whitelist':
        takefromblacklist(call.message)
    if call.data == 'give':
        getidbymessage(call.message)
    if call.data == 'unders':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'admin':
        imgg = open('minimenuimg.PNG', 'rb')
        bot.send_photo(call.message.chat.id,imgg, caption='Администратор для связи:\n'
                                               '@HELPTOURNAMENTS',reply_markup=bback)
    if call.data == 'linkacc':
        bot.send_message(call.message.chat.id, 'Введи свой никнейм Brawl Starts, для того чтобы мы нашли вас.')
        bot.register_next_step_handler(call.message, link_acc)
    if call.data == 'withdraw':
        bot.send_message(call.message.chat.id, 'Вывод временно недоступен.')
    if call.data == 'qiwi':
        bot.send_message(call.message.chat.id, 'Пополнение временно недоступно.')
    if call.data == 'free':
        bot.send_message(call.message.chat.id, 'Пополнение временно недоступно.')
    if call.data == 'umoney':
        bot.send_message(call.message.chat.id, 'Пополнение временно недоступно.')
    if call.data == 'addmoney':
        bot.send_message(call.message.chat.id, 'Введите сумму пополнения:')
        bot.register_next_step_handler(call.message, sendmes)
    if call.data == 'games':
        imgg = open('minimenuimg.PNG', 'rb')
        bot.send_photo(call.message.chat.id,imgg, caption='Выбери тип игры:', reply_markup=gamesmenu)
    if call.data == 'back':
        imgg = open('minimenuimg.PNG', 'rb')
        for value in c.execute(f"SELECT usernames FROM users WHERE chatid = '{call.message.chat.id}'"):
            bot.send_photo(call.message.chat.id, imgg, caption=f'👑 Добро пожаловать, {value[0]}!',
                       reply_markup=minimenu)
        imgg.close()
    if call.data == 'idk':
        bot.send_message(call.message.chat.id, 'Доступные комнаты:', reply_markup=matchesbash)
    if call.data == '1v1':
        bot.send_message(call.message.chat.id, 'Доступные комнаты:', reply_markup=matches1)
    if call.data == '2v2':
        bot.send_message(call.message.chat.id, 'Доступные комнаты:', reply_markup=matches2)
    if call.data == '3v3':
        bot.send_message(call.message.chat.id, 'Доступные комнаты:', reply_markup=matches3)
    if call.data == 'cabin':
        global balance
        for value in c.execute(f"SELECT balance FROM users WHERE chatid = '{call.message.chat.id}'"):
            bal = value[0]
            for value in c.execute(f"SELECT nickname FROM users WHERE chatid = '{call.message.chat.id}'"):
                if value[0] == '?':
                    imgg = open('minimenuimg.PNG', 'rb')
                    bot.send_photo(call.message.chat.id, imgg,caption=f'🆔 Ваш id: {call.message.chat.id}\n'
                                                           f'💰 Баланс: {bal} RUB\n'
                                                           f'♻ Количество игр: 0\n'
                                                           f'💳 Сумма игр: 0 RUB\n'
                                                           f'📊 Рейтинг: ?\n'
                                                           f'Аккаунт Brawl Starts ❌ не привязан.\n', reply_markup=cabmenu)
                else:
                    imgg = open('minimenuimg.PNG', 'rb')
                    bot.send_photo(call.message.chat.id, imgg, caption=f'🆔 Ваш id: {call.message.from_user.id}\n'
                                                       f'💰 Баланс: {bal} RUB\n'
                                                       f'♻ Количество игр: 0\n'
                                                       f'💳 Сумма игр: 0 RUB\n'
                                                       f'📊 Рейтинг: ?\n'
                                                       f'Аккаунт Brawl Starts ✅ привязан.\n', reply_markup=cabmenu)
    if call.data == 'info':
        imgg = open('minimenuimg.PNG', 'rb')
        bot.send_photo(call.message.chat.id, imgg)
        bot.send_message(call.message.chat.id, 'Пользователи сервиса могут поучаствовать в любом турнире, что, согласитесь, очень удобно.\n'
                                               '\n'
                                               'Правила:\n'
                                               '➖ Изменение правил может происходить в любой момент, без уведомления пользователей.\n'
                                               '➖ При игре 1VS1 Боец определяется игроками, если в течении 3 минут они не определились, то в ход вступает рандомайзер\n'
                                               '● При игре 2VS2 Бойцы определяется игроками, если в течении 3 минут они не определились, то в ход вступает рандомайзер.\n'
                                               '● При игре 3VS3 Бойцы определяется игроками. (могут быть полностью разные)\n'
                                               '➖ Если вы присоединились к турниру (Столкновение, 1VS1, 2VS2, 3VS3) но не смогли прийти из-за своих обстоятельств, то возврат средств не подлежит.\n'
                                               '➖ Если по истечению времени подготовки, человек не прожмёт кнопку "готов"  то автоматически происходит кик, без возможности вернуть свои средства.\n'
                                               '➖ Если в турнире 2VS2, 3VS3, человеку не получается прийти и отыграть со своей командой, то турнир отменяется возвращая средства всем игрокам кто ожидал матча, кроме человека, кто сорвал этот турнир.\n'
                                               '➖ Комиссия сервиса 5-10% (в зависимости от турнира) \n'
                                               '➖ Если администратор, или персонал по своей собственной причине не смог провести турнир, тогда деньги на счёт игроков возвращаются. \n'
                                               '➖ Сливать код румы (комнаты) 3 лицам запрещено, бан в боте и кик с турнира, без возможности вывести деньги.\n'
                                               '\n'
                                               'Правила оскорблений:\n'
                                               '➖ Оскорбление Стран, Государств, Властей, Жителей и.т.д запрещено. (4 варна/кик с чата)\n'
                                               '➖ Нацизм запрещен. (кик с чата)\n'
                                               '➖ Оскорбление администрации и работающего персонала запрещено. (3 варна/кик с чата)\n'
                                               '➖ Оскорбление пользователей чата запрещено. (2 варна)\n'
                                               '➖ Оскорбление родных пользователей чата, администрации и рабочим персонала запрещено. (кик с чата)\n'
                                               '➖ Оскорбление проекта запрещено. (кик с чата, канала и бан в боте, при извинение производится разбан только в боте и канале)\n', reply_markup=bbackmenu)



bot.polling()