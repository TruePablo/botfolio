import telebot, os, os.path
from yandex_music import Client

client = Client("AQAAAAAc65qhAAG8XjyfoAhskUCSi6PAgpWv-2I").init()
bot = telebot.TeleBot('5341033103:AAFsG6gYfrTJn98J69SF1USyz4-q37e8QIs')
SRC = 'covers/'
client.init()
type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}


keyboardstart = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardstart.row('Поиск музыки', 'Чарт', 'Помощь')
keyboardchart = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardchart.row('Выбрать и воспроизвести')
keyboardalbum = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardchart.row('Найти весь альбом', 'Назад')
keyboardtex = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardtex.row('Назад')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Это бот для поиска аудио, клипов и т.д.', reply_markup=keyboardstart)

@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text == 'Помощь':
        #Тут вставь свою ссылку        --------------------------\/ сюда
        bot.send_message(message.chat.id, 'Связаться с админом - https://t.me/Resz59', reply_markup=keyboardstart)
    if message.text == 'Тест':
        TOKEN = os.environ.get('AQAAAAAc65qhAAG8XjyfoAhskUCSi6PAgpWv-2I')
        client = Client(TOKEN).init()
        ALBUM_ID = 1106
        album = client.albums_with_tracks(ALBUM_ID)
        tracks = []
        for i, volume in enumerate(album.volumes):
            if len(album.volumes) > 1:
                tracks.append(f'💿 Диск {i + 1}')
            tracks += volume

        text = 'АЛЬБОМ\n\n'
        text += f'{album.title}\n'
        text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
        text += f'{album.year} · {album.genre}\n'

        cover = album.cover_uri
        if cover:
            text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

        text += 'Список треков:'

        bot.send_message(message.chat.id, text)

        for track in tracks:
            if isinstance(track, str):
                bot.send_message(message.chat.id, track)
            else:
                artists = ''
                if track.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in track.artists)
                bot.send_message(message.chat.id, track.title + artists)


    if message.text == 'Текст песни':
        bot.send_message(message.chat.id, 'Раздел в разработке', reply_markup=keyboardstart)
    if message.text == 'Поиск музыки':
        bot.send_message(message.chat.id, 'Введите название песни, которую вы хотите найти:')
        bot.register_next_step_handler(message, send_search_request_and_print_result)
    if message.text == 'Чарт':
        CHART_ID = 'world'
        TOKEN = os.environ.get('AQAAAAAc65qhAAG8XjyfoAhskUCSi6PAgpWv-2I')

        client = Client(TOKEN).init()
        chart = client.chart(CHART_ID).chart

        text = [f'🏆 {chart.title}', chart.description, '', 'Треки:']
        f = 0
        for track_short in chart.tracks:
            track, chart = track_short.track, track_short.chart
            artists = ''
            if track.artists:
                artists = ' - ' + ', '.join(artist.name for artist in track.artists)
            filename = f
            if os.path.exists(f"{filename}.mp3"):
                pass
            #audio = open(f'C:/Users/Paul/PycharmProjects/resposbot/{filename}.mp3', 'rb')
            #bot.send_audio(message.chat.id, audio)
            #audio.close()
            track_text = f'{track.title}{artists}'
            #bot.send_message(message.chat.id, client.tracks_download_info(track_id=track.id, get_direct_links=True))
            if chart.progress == 'down':
                track_text = '🔻 ' + track_text
            elif chart.progress == 'up':
                track_text = '🔺 ' + track_text
            elif chart.progress == 'new':
                track_text = '🆕 ' + track_text
            elif chart.position == 1:
                track_text = '👑 ' + track_text
            track_text = f'{chart.position} {track_text}'
            text.append(track_text)
            f+=1

        bot.send_message(message.chat.id, f'\n'.join(text), reply_markup=keyboardchart)
    if message.text == 'Найти весь альбом':
        bot.send_message(message.chat.id, 'Введите номер трека, к которому вы хотите найти альбом:')
        bot.register_next_step_handler(message, find_album_by_id)
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Вы в главном меню:', reply_markup=keyboardstart)
    if message.text == 'Выбрать и воспроизвести':
        bot.send_message(message.chat.id, 'Введите номер трека:')
        bot.register_next_step_handler(message, senda)

def find_album_by_id(message):
    num = int(message.text)
    CHART_ID = 'world'
    TOKEN = os.environ.get('AQAAAAAc65qhAAG8XjyfoAhskUCSi6PAgpWv-2I')

    client = Client(TOKEN).init()
    chart = client.chart(CHART_ID).chart
    for track_short in chart.tracks:
        track, chart = track_short.track, track_short.chart
        if chart.position != num:
            chart.position += 1
        else:
            ALBUM_ID = track.albums[0].id

            album = client.albums_with_tracks(ALBUM_ID)
            tracks = []
            for i, volume in enumerate(album.volumes):
                if len(album.volumes) > 1:
                    tracks.append(f'💿 Диск {i + 1}')
                tracks += volume

            text = 'АЛЬБОМ\n\n'
            text += f'{album.title}\n'
            text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
            text += f'{album.year} · {album.genre}\n'

            cover = album.cover_uri
            if cover:
                text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

            text += 'Список треков:'

            bot.send_message(message.chat.id, text)

            for track in tracks:
                if isinstance(track, str):
                    bot.send_message(message.chat.id,track)
                else:
                    artists = ''
                    if track.artists:
                        artists = ' - ' + ', '.join(artist.name for artist in track.artists)
                    bot.send_message(message.chat.id, track.title + artists)



def send_search_request_and_print_result(message):
    query = message.text
    search_result = client.search(query)


    try:
        text = [f'Результаты по запросу "{query}":', '']
        best_result_text = ''
        search_result.best.result.download(filename=f'{search_result.best.result.title}.mp3', bitrate_in_kbps=192)
        if search_result.best:
            type_ = search_result.best.type
            best = search_result.best.result

            text.append(f'❗️Лучший результат: {type_to_name.get(type_)}')

            if type_ in ['track', 'podcast_episode']:

                artists = ''
                if best.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in best.artists)
                best_result_text = best.title + artists
            elif type_ == 'artist':
                best_result_text = best.name
            elif type_ in ['album', 'podcast']:
                best_result_text = best.title
            elif type_ == 'playlist':
                best_result_text = best.title
            elif type_ == 'video':
                best_result_text = f'{best.title} {best.text}'

            text.append(f'Содержимое лучшего результата: {best_result_text}\n')
        if search_result.artists:
            text.append(f'Исполнителей: {search_result.artists.total}')
        if search_result.albums:
            text.append(f'Альбомов: {search_result.albums.total}')
        if search_result.tracks:
            text.append(f'Треков: {search_result.tracks.total}')
        if search_result.playlists:
            text.append(f'Плейлистов: {search_result.playlists.total}')
        if search_result.videos:
            text.append(f'Видео: {search_result.videos.total}')

        img = search_result.best.result.downloadCover(filename='cover.png')
        cover = open('cover.png', 'rb')
        bot.send_photo(message.chat.id, cover)
        text.append('')
        bot.send_message(message.chat.id, '\n'.join(text))
        audio = open(f'{search_result.best.result.title}.mp3', 'rb')
        bot.send_audio(message.chat.id, audio, title=search_result.best.result.title, reply_markup=keyboardstart)
        audio.close()

    except:
        bot.send_message(message.chat.id, 'Ошибка, введите другой запрос', reply_markup=keyboardstart)

@bot.message_handler(content_types=['document'])
def senda(message):
    num = int(message.text)
    CHART_ID = 'world'
    TOKEN = os.environ.get('AQAAAAAc65qhAAG8XjyfoAhskUCSi6PAgpWv-2I')

    client = Client(TOKEN).init()
    chart = client.chart(CHART_ID).chart
    for track_short in chart.tracks:
        track, chart = track_short.track, track_short.chart
        if chart.position != num:
            chart.position +=1
        else:
            track.download(filename=f'{track.title}.mp3', bitrate_in_kbps=128)
            audio = open(f'{track.title}.mp3', 'rb')
            img = track.downloadCover(filename='cover.png')
            cover = open('cover.png', 'rb')
            bot.send_photo(message.chat.id, cover)
            bot.send_audio(message.chat.id, audio, reply_markup=keyboardtex)
            audio.close()
           #bot.send_message(message.chat.id, f'Найти альбом трека?{track_short.track.album_id}')
            #bot.send_message(message.chat.id, f'{track.album_id}')

bot.polling()