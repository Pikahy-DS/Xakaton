import datetime
import bs4
import requests
import time
from collections import namedtuple
import urllib.parse
from db_db import *
InnerBlock = namedtuple('Block', 'title, anons,full_text,img,date,url')

class Block(InnerBlock):

    def __str__(self):
        return f'Название: {self.title}\nКраткое описание: {self.anons}\nПолное описание: {self.full_text}\t\nДата размерещения: {self.date}\t\nСсылка: {self.url}\nФото: {self.img}'


class PikabuParser():
    def __init__(self):  # Чтобы не распознали, что мы боты
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Accept-Language': 'ru',
        }
    def get_page(self, page: int = None): # ПРоверяем адрес страницы и так же указываем ссылку на страницу
        url = 'https://www.go31.ru/news'
        r = self.session.get(url)
        return r.text

    def parse_block(self, item):  # переходим на нужный сайт
        url_block = item.select_one('a.c-news-card__title')
        href = url_block.get('href')
        url = href
        title = url_block.get_text('')

        anons_block = item.select_one('div.c-news-card__text') #Тут указываем блок c текстом
        try:
            anons_block = anons_block.get_text('')
            anons_block = str(anons_block).split('.')
            anons_block = anons_block[0]
        except:
            pass
        full_text = item.select_one('div.c-news-card__text')  # Тут указываем блок c текстом
        try:
            full_text = full_text.get_text('')
        except:
            pass
        print(full_text)
        date = item.select_one('div.c-article-info')
        date = date.get_text('')
        try:
            date = date.split('\n')
            time_date = str(date[2]).split(',')
            date = str(time_date[1]).split(' ')
            month = str(date[1])
            month1 = date[:3]
            time_date = str(time_date[0]) + ':00'
            if month == 'Сегодня':
                ic = datetime.datetime.now(tz=None)
                ic = ic.strftime("%Y-%m-%d")
                date = ic + ' ' + time_date
            elif month == 'Вчера':
                ic = datetime.datetime.now(tz=None)
                ic = ic.strftime("%Y-%m-%d")
                iv = datetime.datetime.now(tz=None).strftime("%Y-%m-")
                day = int(ic[8:10])
                day = day - 1
                date = iv + str(day) + ' ' + time_date
            else:
                month1 = date[2]
                months_map = {
                    'январь': 1,
                    'февраль': 2,
                    'апреля': 4,
                    'мая': 5,
                    'июня': 6,
                    'июля': 7,
                    'августа': 8,
                    'сентября': 9,
                    'октября': 10,
                    'марта': 3,
                    'ноября': 11,
                    'декабря': 12,
                }
                month = months_map.get(month1)
                date = '2020-'+ str(month)+ '-' + str(date[1]) + ' ' + str(time_date)

        except:
            pass
        try:
            img = ' '

        except:
            pass


        if img == None:
            img = str(' ')
        return Block(
            url = url,
            title = title,
            anons = anons_block,
            full_text = full_text,
            img = img,
            date = date,
        )

    def get_block(self, page: int = None): #Основной цикл где все происходит
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.c-news-card')
        i = 0
        for item in container:
            block = self.parse_block(item = item)
            if block.date == None or block.anons == None :
                continue

            init_db()
            add_message(title = block.title, anons=block.anons,
                       full_text=block.full_text, img=block.img, date=block.date)
            print(block)


def main():
    p = PikabuParser()
    p.get_block()


if __name__ == '__main__':
    main()