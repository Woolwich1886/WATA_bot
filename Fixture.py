from lxml import etree
import requests
from datetime import datetime, timedelta
import re


def find_next_game():

    # Сайт ФК Арсенал
    fixturer = requests.get('https://www.arsenal.com/')
    parser = etree.HTMLParser()
    root = etree.fromstring(fixturer.text, parser)
    # Расположение информации о следующей игре на сайте клуба
    match_info = root[1][2][0][4][2][3][0]
    # Дата, стадион, команда хозяев, команда гостей, наименование турнира
    match_date = match_info[0][1][0].text
    match_place = match_info[0][1][1].text
    match_home = match_info[1][0][0][0][1][0][0].text
    match_away = match_info[1][0][2][0][1][0][0].text
    match_competition = match_info[0][1][3].text
    # разделение даты игры, так как у нее формат 'Sat Jul 6 - 15:00'
    dt = match_date.split()
    month = dt[1]
    day = dt[2]
    hrs = dt[-1].split(':')[0]
    mnts = dt[-1].split(':')[1]
    # формирование приемлемого вида даты для datetime
    # и костыль с годом на текущий сезон 2019-2020
    if month == 'Jan':
        month = 1
        year = 2020
    elif month == 'Feb':
        month = 2
        year = 2020
    elif month == 'Mar':
        month = 3
        year = 2020
    elif month == 'Apr':
        month = 4
        year = 2020
    elif month == 'May':
        month = 5
        year = 2020
    elif month == 'Jun':
        month = 6
        year = 2019
    elif month == 'Jul':
        month = 7
        year = 2019
    elif month == 'Aug':
        month = 8
        year = 2019
    elif month == 'Sep':
        month = 9
        year = 2019
    elif month == 'Oct':
        month = 10
        year = 2019
    elif month == 'Nov':
        month = 11
        year = 2019
    elif month == 'Dec':
        month = 12
        year = 2019
    # прибавление двух часов, чтобы выводилось время по Москве
    fixture_time = datetime(year, month, int(day), int(hrs), int(mnts)) + timedelta(hours=2)
    data = re.findall(r'[\w]+', str(fixture_time))
    data_y = data[0]
    data_d = data[2]
    data_h = data[3]
    data_min = data[4]
    # дополнительная информация в виде дня недели
    if fixture_time.isoweekday() == 1:
        data_wd = 'Понедельник'
    elif fixture_time.isoweekday() == 2:
        data_wd = 'Вторник'
    elif fixture_time.isoweekday() == 3:
        data_wd = 'Среда'
    elif fixture_time.isoweekday() == 4:
        data_wd = 'Четверг'
    elif fixture_time.isoweekday() == 5:
        data_wd = 'Пятница'
    elif fixture_time.isoweekday() == 6:
        data_wd = 'Суббота'
    elif fixture_time.isoweekday() == 7:
        data_wd = 'Воскресенье'
    # вывод месяца в виде слова
    if data[1] == '01':
        data_m = 'январь'
    elif data[1] == '02':
        data_m = 'февраль'
    elif data[1] == '03':
        data_m = 'март'
    elif data[1] == '04':
        data_m = 'апрель'
    elif data[1] == '05':
        data_m = 'май'
    elif data[1] == '06':
        data_m = 'июнь'
    elif data[1] == '07':
        data_m = 'июль'
    elif data[1] == '08':
        data_m = 'август'
    elif data[1] == '09':
        data_m = 'сентябрь'
    elif data[1] == '10':
        data_m = 'октябрь'
    elif data[1] == '11':
        data_m = 'ноябрь'
    elif data[1] == '12':
        data_m = 'декабрь'

    return 'Дата: ' + data_wd + ' ' + data_d + ' ' + data_m + ' ' + data_y + '\n' + \
           'Время (МСК): ' + data_h + '-' + data_min + '\n' + \
           'Стадион: ' + match_place + '\n' \
           + match_home + ' - ' + match_away + \
           '\n' + match_competition