#Подключение библиотек и API
import telebot
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageDraw, ImageFont
from PIL import ImageChops
from PIL import ImageFilter

#Токены API, переменные и пр.
bot = telebot.TeleBot('5370061736:AAESR-sRMx1XEtNMA6BezRddokUWza_2_pQ')
SOURCE_DIR = 'imgs/'

#Клавиатуры
keyboardstart = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardstart.row('Обработать изображение', 'Помощь')

keyboardback = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardback.row('Назад')

keyboardhelp = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardhelp = keyboardhelp.row('Связаться с админом', 'Назад')

keyboardwork = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardwork = keyboardwork.row('Кадрировать', 'Повернуть', 'Водяной знак', 'Ч/Б', 'Текст для знака', 'Фильтры', 'Инста', 'Назад')

keyboardrotate = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardrotate = keyboardrotate.row('Повернуть влево', 'Повернуть вправо', 'Назад')

keyboardfiltr = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardfiltr.row('Темнее', 'Резкость', 'Назад')

#Команда старт
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Это бот для редактирования фотографий', reply_markup=keyboardstart)


#Ответ на сообщения
@bot.message_handler(content_types=['text'])
def send_message(message):
    global SOURCE_DIR
    if message.text == 'Помощь':
        bot.send_message(message.chat.id, 'Тут будет инструкция по использованию', reply_markup=keyboardhelp)
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню', reply_markup=keyboardstart)
    if message.text == 'Обработать изображение':
        bot.send_message(message.chat.id, 'Меню обработки изображения:', reply_markup=keyboardwork)
    if message.text == 'Кадрировать':
        bot.send_message(message.chat.id, 'Отправьте фото в формате .jpg',reply_markup=keyboardback)
        bot.register_next_step_handler(message, handle_docs_photo)
    if message.text == 'Связаться с админом':
        bot.send_message(message.chat.id, 'https://t.me/MaRozalina', reply_markup=keyboardhelp)
    if message.text == 'Ч/Б':
        bot.send_message(message.chat.id, 'Отправьте фото в формате .jpg',reply_markup=keyboardback)
        bot.register_next_step_handler(message, bw)
    if message.text == 'Повернуть':
        bot.send_message(message.chat.id, 'Отправьте фото в формате .jpg',reply_markup=keyboardback)
        bot.register_next_step_handler(message, retright)
    if message.text == 'Повернуть влево':
        bot.send_message(message.chat.id, 'Отправьте файл ещё раз',reply_markup=keyboardback)
        bot.register_next_step_handler(message, retleft)
    if message.text == 'Повернуть вправо':
        bot.send_message(message.chat.id, 'Отправьте файл ещё раз',reply_markup=keyboardback)
        bot.register_next_step_handler(message, retright)
    if message.text == 'Водяной знак':
        bot.send_message(message.chat.id, 'Отправьте фото в формате .jpg',reply_markup=keyboardback)
        bot.register_next_step_handler(message, add_watermark)
    if message.text == 'Текст для знака':
        bot.send_message(message.chat.id, 'Введите текст для изображения:',reply_markup=keyboardback)
        bot.register_next_step_handler(message, imgtext)
    if message.text == 'Фильтры':
        bot.send_message(message.chat.id, 'Выберите фильтр:', reply_markup=keyboardfiltr)
    if message.text == 'Инста':
        bot.send_message(message.chat.id, 'Отправьте фото как файл:', reply_markup=keyboardback)
        bot.register_next_step_handler(message, insta)
    if message.text == 'Темнее':
        bot.send_message(message.chat.id, 'Отправьте фото как файл:')
        bot.register_next_step_handler(message, fil1)
    if message.text == 'Резкость':
        bot.send_message(message.chat.id, 'Отправьте фото как файл:')
        bot.register_next_step_handler(message, fil2)

#Обработка под инсту
def insta(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = SOURCE_DIR + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        p1 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
        if p1.height < p1.width:
            p1 = p1.crop((p1.width // 4, 0, p1.width - (p1.width // 4), p1.height))
            p1.save(SOURCE_DIR + f'{message.document.file_name}')
        canvas = Image.new(p1.mode, (p1.height, p1.height))
        temp = p1.resize((p1.height, p1.height))
        temp = temp.filter(ImageFilter.GaussianBlur(30))
        canvas.paste(temp, (0, 0))
        canvas.paste(p1, ((p1.height-p1.width) // 2, 0))
        canvas = canvas.rotate(270)
        bot.send_photo(message.chat.id, canvas)
#Фильтры:
def fil1(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = SOURCE_DIR + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        p1 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
        p2 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
        result = ImageChops.hard_light(p1, p2)
        bot.send_photo(message.chat.id, result)
def fil2(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = SOURCE_DIR + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        p1 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
        result = p1.filter(ImageFilter.SHARPEN)
        result = result.filter(ImageFilter.SHARPEN)
        bot.send_photo(message.chat.id, result)
def imgtext(message):
    bot.send_message(message.chat.id, 'Введите текст для водяного знака.')
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return
    sample = message.text
    image = Image.new("RGB", (75, 50), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("timesnewromanpsmt.ttf", 20, encoding='UTF-8')
    draw.text((10, 10), sample, font=font, fill='black')
    image.save(SOURCE_DIR + 'sample.png')
    sai = Image.open(SOURCE_DIR + 'sample.png')
    sai = sai.convert("RGBA")
    datas = sai.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    sai.putdata(newData)
    sai.save(SOURCE_DIR + 'sample.png')
    bot.send_message(message.chat.id, 'Получен текст:', reply_markup=keyboardwork)
    bot.send_photo(message.chat.id, sai)

@bot.message_handler(content_types=['document'])
#Кадрирование фото
def handle_docs_photo(message):
    chat_id = message.chat.id
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = SOURCE_DIR + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            p1 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
            size = p1.size
            w, h = size
            cropped = p1.crop((w/4,h/4,w/2,h/2))
            bot.send_photo(chat_id, cropped)
            bot.send_message(message.chat.id, f"Вот кадрированное фото:", reply_markup=keyboardwork)
    except:
            bot.send_message(chat_id, 'Неизвестная ошибка, попробуйте снова.')
def bw(message):
    chat_id = message.chat.id
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = SOURCE_DIR + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            p1 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
            bwimg = p1.convert('L')
            bot.send_photo(chat_id, bwimg)
            bot.send_message(chat_id, 'Вот изображение в черно-белом варианте', reply_markup=keyboardwork)
    except AttributeError:
        bot.send_message(chat_id, 'Ошибка, отправьте фото как файл')
        bot.register_next_step_handler(message, bw)
def add_watermark(message, opacity=1, wm_interval=0):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return
    watermarks = SOURCE_DIR + 'sample.png'
    watermark = Image.open(watermarks)
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = SOURCE_DIR + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            p1 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
        assert opacity >= 0 and opacity <= 1
        if opacity < 1:
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            else:
                watermark = watermark.copy()
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark.putalpha(alpha)
        layer = Image.new('RGBA', p1.size, (0,0,0,0))
        for y in range(0, p1.size[1], watermark.size[1]+wm_interval):
            for x in range(0, p1.size[0], watermark.size[0]+wm_interval):
                layer.paste(watermark, (x, y))
        fimg = Image.composite(layer,  p1,  layer)
        bot.send_message(message.chat.id, 'Фото с водяным знаком:', reply_markup=keyboardwork)
        bot.send_photo(message.chat.id, fimg)
    except AttributeError:
        bot.send_message(message.chat.id, 'Ошибка, отправьте фото как файл')
        bot.register_next_step_handler(message, add_watermark)
def retleft(message):
    chat_id = message.chat.id
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = SOURCE_DIR + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            p1 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
            rimg = p1.rotate(-90)
            bot.send_photo(chat_id, rimg)
            bot.send_message(chat_id, 'Вот перевенутое фото', reply_markup=keyboardrotate)
    except AttributeError:
        bot.send_message(chat_id, 'Ошибка, отправьте фото как файл')
        bot.register_next_step_handler(message, retright)
def retright(message):
    chat_id = message.chat.id
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboardwork)
        return 
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = SOURCE_DIR + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            p1 = Image.open(SOURCE_DIR + f'{message.document.file_name}')
            rimg = p1.rotate(90)
            bot.send_photo(chat_id, rimg)
            bot.send_message(chat_id, 'Вот перевенутое фото', reply_markup=keyboardrotate)
    except AttributeError:
        bot.send_message(chat_id, 'Ошибка, отправьте фото как файл')
        bot.register_next_step_handler(message, retright)

bot.polling() #Запуск бота