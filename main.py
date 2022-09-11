import requests
from bs4 import BeautifulSoup as BS
import re
from datetime import date
from DataOxTestTask import db_connection

titles = []
descriptions = []
locations = []
dates = []
prices = []
currencies = []
images = []
bedrooms = []

def get_title(main):
    global titles
    titles_code = main.findAll('div', class_='title')
    for title in titles_code:
        titles.append(title.text.strip())

def get_description(main):
    global descriptions
    descriptions_code = main.findAll('div', class_='description')
    for description in descriptions_code:
        descriptions.append(description.text.strip().split('\n')[0])

def get_location(main):
    global locations
    global dates
    locations_code = main.findAll('div', class_='location')
    for location in locations_code:
        locations.append(location.text.strip().split('\n')[0])
        date_of_published = location.text.strip().split('\n')[-1]
        date_pattern = re.compile(r'\d+/\d+/\d+')
        if date_pattern.match(date_of_published) is not None:
            date_of_published = date_of_published.split('/')
            date_of_published = [int(i) for i in date_of_published]
            date_of_published = date.strftime(date(date_of_published[2], date_of_published[1], date_of_published[0]), '%d-%m-%y')
        else:
            date_of_published = date.today().strftime('%d-%m-%y')
        dates.append(str(date_of_published))


def get_price(main):
    global prices
    global currencies
    prices_code = main.findAll('div', class_='price')
    for price in prices_code:
        currencies.append(re.split('', price.text.strip(), 2)[1])
        prices.append(re.split('', price.text.strip(), 2)[2])


def get_image(main):
    global images
    images_code = main.findAll('div', class_='image')
    for image in images_code:
        img = image.find('img')
        images.append(img['src'])

def get_bedroom(main):
    global bedrooms
    bedrooms_code = main.findAll('span', class_='bedrooms')
    for bedroom in bedrooms_code:
        bed = bedroom.text.strip().split('\n')
        bedrooms.append(bed[0] + bed[1].replace(' ', ''))


if __name__ == '__main__':
    # try:
    #     n = 1
    #     for i in range(1, 95):
    #         url = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page={i}/c37l1700273'
    #         res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'})
    #         soup = BS(res.text, 'html.parser')
    #         main = soup.find('main')
    #         get_title(main)
    #         get_location(main)
    #         get_description(main)
    #         get_price(main)
    #         get_image(main)
    #         get_bedroom(main)
    #         n += 1
    #         print(n)
    # except Exception as ex:
    #     db_connection.insert_elements(titles, locations, dates, prices, currencies, images, bedrooms, descriptions)
    #     db_connection.select_elements()
    db_connection.dump_to_xlsx()
