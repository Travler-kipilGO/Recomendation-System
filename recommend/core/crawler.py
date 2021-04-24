import requests
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import urlopen
import datetime
import time

class AccommodationList:
    def __init__(self, keyword, adult=2, children=0, rooms=1):
        self.keyword = keyword
        self.chekin_date = datetime.datetime.now()
        self.chekout_date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.adult = adult
        self.children = children
        self.rooms = rooms
        self.list = list()

    def getAccommodationList(self, offset=0):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            "Accept-Language": "ko-KR"
        }
        offset = offset * 25
        query = {
            'ss': self.keyword,
            'checkin_year':self.chekin_date.year,
            'checkin_month':self.chekin_date.month,
            'checkin_monthday':self.chekin_date.day,
            'checkout_year':self.chekout_date.year,
            'checkout_month':self.chekout_date.month,
            'checkout_monthday':self.chekout_date.day + 1,
            'group_adults':self.adult,
            'group_children':self.children,
            'no_rooms':self.rooms,
            'top_ufis':1,
            'rows':25,
            'offset':offset
        }

        params = parse.urlencode(query, encoding='UTF-8') 
        url = 'https://www.booking.com/searchresults.ko.html?'+params

        res = requests.get(url, headers = headers)
        time.sleep(2)

        soup = BeautifulSoup(res.text, 'lxml')
        
        item_list = soup.select('div.sr_item')
        for item in item_list:
            get_href = item.select_one('a.hotel_name_link').get('href')
            name = item.select_one('span.sr-hotel__name').get_text(strip=True)
            detail_url = f'https://www.booking.com{get_href}'
            detail_url = detail_url.replace("\n", "")
            hotel_img = item.select_one('img.hotel_image').get('src')
            accommodation = AccommodationDetail(
                keyword=self.keyword,
                name=name,
                hotel_img=hotel_img,
                detail_url=detail_url,
            )
            self.list.append(accommodation)
            

class AccommodationDetail:
    def __init__(self, keyword, name, hotel_img, detail_url):
        self.keyword = keyword
        self.name = name
        self.hotel_img = hotel_img
        self.detail_url = detail_url
        self.location = ''
        self.thub_img_list = []
        self.img_list = []
        self.room_list = []

    def getAccommodationDetail(self):
        try:
            headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
            url = self.detail_url
            res = requests.get(url, headers = headers)
            print(res.status_code)
            time.sleep(5)
        except Exception as e:
            print(type(e))    
            print(e.args)     
            print(e) 

        else:
            if str(type(res)) == "<class 'requests.models.Response'>" and res.status_code == 200:
                soup = BeautifulSoup(res.text, 'lxml')

                self.location = soup.select_one('span.hp_address_subtitle').get_text(strip=True)

                main = soup.find('div', id='hotel_main_content')
                img_container = main.select_one('div.bh-photo-grid')
                imgs = img_container.select('a.bh-photo-grid-item')
                for img in imgs:
                    try:
                        self.thub_img_list.append(img.get('href'))
                        self.img_list.append(img.select_one('img').get('src'))
                    except:
                        pass

                try:
                    rooms_container = soup.find('table', id='hprt-table')
                    rooms = rooms_container.select('tr.js-rt-block-row')
                    for room in rooms:
                        name = room.select_one('div.hprt-roomtype-block').get_text(strip=True)
                        price = room.select_one('div.bui-price-display__value').get_text(strip=True)
                        guest = room.select_one('span.bui-u-sr-only').get_text(strip=True)
                        self.room_list.append([name, price, guest])
                except:
                    pass 