import requests
import pandas as pd
import re
import os
from requests import get
from random import randint
from time import time
from warnings import warn
from time import sleep
from bs4 import BeautifulSoup
from IPython.core.display import clear_output


start_time = time()
r=0

site_url = 'https://info.1cont.ru/contragent/search/?type=ul&query=Топливо&inactive=0'

req = requests.get(site_url)
html_soup = BeautifulSoup(req.text, 'html.parser')

agents_info = html_soup.find_all('div', class_='u-left')
requisites_info = html_soup.find_all('div', class_='u-right')

names_list = []
company_list = []
adress_list = []
okved_list = []

region_list = []
ogrn_list = []
inn_list = []

url_1 = 'https://info.1cont.ru/'

def count_pages(url):
    global previous
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    pages_amount = soup.find('div', attrs={'class': 'pagination-container'}).text.strip()
    last_shown = (pages_amount.split()[-1])

    if last_shown == 'Следующая':
        url = url.replace('&page=' + str(last_shown), ' ')
        previous = pages_amount.split()[-2]
        url = url + '&page=' + str(previous)
        count_pages(url)

    return previous


amount_of_pages = count_pages(site_url)
print(amount_of_pages)


pages = [str(i) for i in range(1, int(amount_of_pages))]

for page in pages:
    print("Processing over the page " , page)
    url = ("https://info.1cont.ru/contragent/search/?type=ul&inactive=0&query=Топливо&page=" + page)
    response = get(url)
    print(response)

    sleep(randint(8, 15))

    # Monitor the requests
    r += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(r, r / elapsed_time))
    clear_output(wait=True)

    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(r, response.status_code))

        # Break the loop if the number of requests is greater than expected
    if r > 72:
        warn('Number of requests was greater than expected.')
        break

    html_soup = BeautifulSoup(response.text, 'html.parser')

    agents_info = html_soup.find_all('div', class_='u-left')
    requisites_info = html_soup.find_all('div', class_='u-right')

    for agents in agents_info:
        personal_name = agents.find('div', attrs={'class': 'u-ceo'}).text.strip()
        names_list.append(personal_name)
        adress = agents.find('div', attrs={'class': 'u-address'}).text.strip()
        adress_list.append(adress)
        company_type = agents.find('span', attrs={'class': 'und'}).text.strip()
        company_list.append(company_type)

        # переходим по ссылке внутри таблицы и получаем ОКВЭД
        for link in agents.find_all('a'):
            url_link = (url_1 + link.get('href'))
            req_l = requests.get(url_link)
            req_l = BeautifulSoup(req_l.text, 'html.parser')
            okved = req_l.find('h2', attrs={'class': 'big-description'}).text.strip()
            if okved == ('Основной вид деятельности не указан') or okved== None:
                okved_list.append(0)
            else:
                okved = (re.findall(r'\d+', okved))[0] + '.' + (re.findall(r'\d+', okved))[1]
                okved_list.append(okved)
#
    for agents in requisites_info:
        region = agents.find('div', attrs={'class': 'u-region'}).text.strip()
        requisites = agents.find('div', attrs={'class': 'u-requisites'}).text.strip()
        ogrn = (re.findall(r'\d+', requisites))[0]
        inn = (re.findall(r'\d+', requisites))[1]
        region_list.append(region)
        ogrn_list.append(ogrn)
        inn_list.append(inn)



test_df = pd.DataFrame(
    {'Юр. лицо': company_list, 'ФИО': names_list, 'Адресс': adress_list, 'Регион': region_list, 'ОГРН ': ogrn_list,
     'ИНН': inn_list, 'Основной вид деятельности': okved_list

     })


print(test_df)
test_df.to_csv("data_by_query.csv", sep=',', index=False)
