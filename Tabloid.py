from lxml import etree
import requests
from PIL import Image, ImageDraw


def paint_table():

    # Сайт Английской Премьер Лиги
    tttable = requests.get('https://www.premierleague.com/tables')
    parser = etree.HTMLParser()
    root = etree.fromstring(tttable.text, parser)

    # Место, где находится информация по таблице
    tablo = root[1][1][3][3][0][0][0][0][2]

    # У каждой команды есть скрытое подменю
    # 'К' нужно для того, чтобы взять только нечетные результаты поиска
    # то есть только сами команды

    k = 0
    # Словарь со значениями для каждой команды по ключам
    # соответсвтующим значениям таблицы

    table_res = {
        'position': [],
        'team': [],
        'games': [],
        'W': [],
        'D': [],
        'L': [],
        'GD': [],
        'points': []
    }

    # Добавление значений в словарь
    for i in tablo:
        k += 1
        if k % 2 != 0:
            table_res['position'] += [i[1][0].text]
            table_res['team'] += [i[2][0][1].text]
            table_res['games'] += [i[3].text]
            table_res['W'] += [i[4].text]
            table_res['D'] += [i[5].text]
            table_res['L'] += [i[6].text]
            table_res['GD'] += [i[9].text.strip()]
            table_res['points'] += [i[10].text]

    # процесс рисования таблицы для отправки картинкой
    txt = Image.new("RGBA", (320, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    v = 15
    h = 170
    d.text((0, 3), 'pos', fill=(0, 0, 0, 255))
    d.text((30, 3), 'Team', fill=(0, 0, 0, 255))
    d.text((150, 3), 'Games', fill=(0, 0, 0, 255))
    d.text((190, 3), 'W', fill=(0, 0, 0, 255))
    d.text((210, 3), 'D', fill=(0, 0, 0, 255))
    d.text((230, 3), 'L', fill=(0, 0, 0, 255))
    d.text((250, 3), 'GD', fill=(0, 0, 0, 255))
    d.text((270, 3), 'Pts', fill=(0, 0, 0, 255))

    # Если команда - Арсенал, то выделяет строку
    for i in table_res['team']:
        if i == 'Arsenal':
            d.rectangle(((0, v), (320, v+15)), fill='yellow')
        d.text((15, v), i, fill=(0, 0, 0, 255))
        v += 15
    v = 15
    for i in table_res['position']:
        d.text((0, v), i, fill=(0, 0, 0, 255))
        v += 15
    v = 15
    keys = ['games', 'W', 'D', 'L', 'GD', 'points']
    for key in keys:
        for i in table_res[key]:
            d.text((h, v), i, fill=(0, 0, 0, 255))
            v += 15
        v = 15
        h += 20
    del d
    txt.save("test.png", "PNG")
