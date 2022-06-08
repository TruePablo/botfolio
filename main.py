import telebot
from random import randint
import time
import sqlite3
from PIL import Image
from threading import Timer
i = 0
schet = 0
usv = 0
voteusernames = []
locations = ['Театр', 'Парк', 'Водохранилище', 'Кинотеатр', 'Фудкорт', 'Торговый центр', 'Спортивный зал', 'Теннисная площадка', 'Гольф клуб', 'Аэропорт', 'Вокзал']
roles = ['Шпион', 'Игрок']
roundd = 300 #ВРЕМЯ НА ОБСУЖДЕНИЯ
bot = telebot.TeleBot('5255792657:AAF0rzFZooH_Tc50CfMJyGcv7-HS-Jw3X1A') #ТОКЕН БОТА

#Создание базы данных
db = sqlite3.connect('server.db', check_same_thread=False)
curs = db.cursor()
curs.execute("""CREATE TABLE IF NOT EXISTS users (
	username TEXT,
	chatid BIGINT,
	user TEXT
)""")
print('DB created/found')
db.commit()


#КЛАВИАТУРЫ, ОБЬЯВЛЕНИЯ
keyboardstart = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardstart.row('Начать игру', 'Помощь')

keyboardgame = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardgame.row('Запуск', 'Назад', 'Список')

keyboardgame1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardgame1.row('Вернуться к игре', 'Помощь')

keyboardv = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardv.row('Досрочное голосование')

keyboardhelp = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardhelp.row('Связаться с админом', 'Назад')

print('all started successful')
#/start
@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Это бот для игры в "Шпиона"', reply_markup=keyboardstart) #keyboardstart

#Всё остальное
@bot.message_handler(content_types=['text'])
def send_message(message):
	global usv
	global usern
	global voteusernames
	global schet
	global i
	if message.text == 'Тест':
		i = 0
		bot.send_message(message.chat.id, 'Запущено', reply_markup=keyboardv)
		while i < 5:
			i += 1
			time.sleep(1)
			print(i)
		if i == 5:
			bot.send_message(message.chat.id, 'Остановлено по таймеру')
	if message.text == 'Досрочное голосование':
		i = 350
	if message.text == 'Вернуться к игре':
		bot.send_message(message.chat.id, 'Ожидаем других игроков, нажмите запуск когда все будут готовы', reply_markup=keyboardgame)

	if message.text == 'Запуск':
		if usv < 2:
			bot.send_message(message.chat.id, f'Недостаточное количество игроков {usv}', reply_markup=keyboardgame)
		else:
			relocate = locations[randint(0, len(locations) - 1)]
			for value in curs.execute("SELECT chatid FROM users"):
				userrole = roles[randint(0, 1)]
				spys = 0
				if usv < 5 and spys < 3:
					if userrole == 'Игрок':
						bot.send_message(value[0], f'Вы - игрок, ваша локация: {relocate}', reply_markup=keyboardv)
						relocateimage(relocate, value[0])
					else:
						spys += 1
						bot.send_message(value[0], 'Вы - шпион', reply_markup=keyboardv)
				else:
					bot.send_message(value[0], f'Вы - игрок, ваша локация: {relocate}', reply_markup=keyboardv)
					relocateimage(relocate, value[0])

			i = 0
			while i < 300:
				i += 1
				time.sleep(1)
				print(i)
			if i == 300:
				for value in curs.execute("SELECT chatid FROM users"):
					keyboardvote = telebot.types.ReplyKeyboardMarkup(True, True)
					for value in curs.execute("SELECT username FROM users"):
						voteusernames.insert(schet, value[0])
						schet += 1
						keyboardvote.row(value[0])
					for value in curs.execute("SELECT chatid FROM users"):
						bot.send_message(value[0], 'Время вышло! Кого вы считаете шпионом? Выберете кнопкой или введите имя пользователя', reply_markup=keyboardvote)
			else:
				for value in curs.execute("SELECT chatid FROM users"):
					keyboardvote = telebot.types.ReplyKeyboardMarkup(True, True)
					for value in curs.execute("SELECT username FROM users"):
						voteusernames.insert(schet, value[0])
						schet+=1
						keyboardvote.row(value[0])
					for value in curs.execute("SELECT chatid FROM users"):
						bot.send_message(value[0], 'Досрочное голосование! Кого вы считаете шпионом? Выберете кнопкой или введите имя пользователя', reply_markup=keyboardvote)


	if message.text == 'Список':
		for value in curs.execute("SELECT username FROM users"):
			bot.send_message(message.chat.id, f'{str(value[0])}', reply_markup=keyboardgame)


	if message.text == 'Начать игру':
		bot.register_next_step_handler()
		 #game




	if message.text == 'Назад':
		bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardgame1)

	if message.text == 'Помощь':
		bot.send_message(message.chat.id, "Игра шпион. Перед игрой необходимо создать группу с пользователями, кто будет играть. Когда все игроки будут зарегестрированы, любой из участников может запустить игру нажав кнопку ЗАПУСК", reply_markup=keyboardhelp)

	if message.text == 'Связаться с админом':
		bot.send_message(message.chat.id, 'https://t.me/efimov_111', reply_markup=keyboardstart)

	if message.text in voteusernames:
		bot.send_message(message.chat.id, f'Мы удалим юзера {message.text} из игры,', reply_markup=keyboardstart)
		curs.execute(f"DELETE FROM users WHERE username = '{message.text}'")
		db.commit()

def userr(message):
	user = message.text
	global usv, usern
	usv += 1
	usern = message.from_user.username
	curs.execute(f"SELECT username FROM users WHERE username = '{usern}'")
	if curs.fetchone() is None:
		curs.execute(f"INSERT INTO users VALUES ('{usern}', {message.chat.id}, {user})")
		db.commit()
		bot.send_message(message.chat.id, f'Вы зарегестрировались на игру под ником {user}', reply_markup=keyboardgame)
	bot.send_message(message.chat.id, f'Вы зарегестрированы на игру под ником {user}, когда все игроки будут готовы нажмите "Запуск"', reply_markup=keyboardgame)

@bot.message_handler(content_types=['document'])
def relocateimage(relocate, value):
	dir = 'locations/'
	match relocate:
		case 'Театр':
			p1 = Image.open(dir + 'Theatre.jpg')
			bot.send_photo(value, p1)
		case 'Парк':
			p1 = Image.open(dir + 'thepark.jpg')
			bot.send_photo(value, p1)
		case 'Водохранилище':
			p1 = Image.open(dir + 'water.jpg')
			bot.send_photo(value, p1)
		case 'Кинотеатр':
			p1 = Image.open(dir + 'cinema.jpg')
			bot.send_photo(value, p1)
		case 'Фудкорт':
			p1 = Image.open(dir + 'thepark.jpg')
			bot.send_photo(value, p1)
		case 'Торговый центр':
			p1 = Image.open(dir + 'centre.jpg')
			bot.send_photo(value, p1)
		case 'Спортивный зал':
			p1 = Image.open(dir + 'gym.jpg')
			bot.send_photo(value, p1)
		case 'Теннисная площадка':
			p1 = Image.open(dir + 'tennis_court.jpg')
			bot.send_photo(value, p1)
		case 'Гольф клуб':
			p1 = Image.open(dir + 'golfclub.jpg')
			bot.send_photo(value, p1)
		case 'Аэропорт':
			p1 = Image.open(dir + 'airport.jpg')
			bot.send_photo(value, p1)
		case _:
			p1 = Image.open(dir + 'train.jpg')
			bot.send_photo(value, p1)

bot.polling()