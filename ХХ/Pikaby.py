import datetime
import bs4
import requests
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
        url = 'https://pikabu.ru/search?t=Белгород&st=1&vn=false'
        r = self.session.get(url)
        return r.text

    def parse_block(self, item):  # переходим на нужный сайт
        url_block = item.select_one('div.story__main')
        url_block = url_block.select_one('a.story__title-link')
        href = url_block.get('href')
        url = href

        title_block = item.select_one('h2.story__title') #Тут указываем блок с текстом
        title = title_block.string.strip()

        anons_block = item.select_one('div.story-block.story-block_type_text') #Тут указываем блок c текстом
        try:
            anons_block = anons_block.get_text('')
        except:
            pass
        full_text = item.select_one('div.story-block.story-block_type_text')  # Тут указываем блок c текстом
        try:
            full_text = full_text.get_text('')
        except:
            pass
        date = item.select_one('div.user__info.user__info_left')
        date = date.select_one('time')
        try:
            date = date.get('datetime')
        except:
            pass
        #date = date.select_one('datetime')
        try:
            date = date.split('T')
            time_date = str(date[1]).split('+')
            time_date = time_date[0]
            date = date[0]
            date = date + ' ' + time_date
        except:
            pass
        try:
            img = item.select_one('div.story-image__content.image-lazy')
            img = img.select_one('img')
            img = str(img.get('data-large-image'))

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
        container = soup.select('article.story')
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