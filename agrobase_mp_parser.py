import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

""" ПАРСИНГ ДАННЫХ С САЙТА ПО ВСЕМ ОКРУГАМ"""

site_url = 'https://www.agrobase.ru/selxozpredpriyatiya/rossiya'
districts = []

name_list = []
fax_list = []
adress_list = []
person_list = []
telefone_list = []
activity_list = []

req = requests.get(site_url)
soup = BeautifulSoup(req.text, 'html.parser')

site = 'https://www.agrobase.ru/'
ref = soup.find('div', class_='clearfix')
all_urls = ref.find_all('a')

for url in all_urls:
    okrug = url.text.strip()
    print(okrug)

    url_link = (site + url.get('href'))
    req_l = requests.get(url_link)
    html_soup = BeautifulSoup(req_l.text, 'html.parser')

    agents_info = html_soup.find_all('div', class_='ac-company')
    for agents in agents_info:
        name = agents.find('p', attrs={'class': 'ac-company__name'}).text.strip()
        name_list.append(name)
        districts.append(okrug)
        # -------
        try:
            fax = agents.find('dl', class_='ac-company__details').find('dt', text='Факс:').find_next_sibling('dd').text
            fax_list.append(fax)
        except:
            fax_list.append(0)
        # -------
        try:
            activity = agents.find('dl', class_='ac-company__details').find('dt',
                                                                            text='Вид деятельности:').find_next_sibling(
                'dd').text
            activity_list.append(activity)
        except:
            activity_list.append(0)
        # --------
        try:
            adress = agents.find('dl', class_='ac-company__details').find('dt', text='Адрес:').find_next_sibling(
                'dd').text

            adress_list.append(adress)
        except:
            adress_list.append(0)
        # --------
        try:
            telefone = agents.find('dl', class_='ac-company__details').find('dt', text='Телефон:').find_next_sibling(
                'dd').text
            telefone_list.append(telefone)
        except:
            telefone_list.append(0)
        # --------
        try:
            person = agents.find('dl', class_='ac-company__details').find('dt', text='Руководство:').find_next_sibling(
                'dd').text
            person_list.append(person)
        except:
            person_list.append(0)

test_df = pd.DataFrame(
    {'Сх Предприятие': name_list, 'Руководитель': person_list, 'Адрес': adress_list, 'Телефон': telefone_list,
     "Факс": fax_list, 'Вид деятельности ': activity_list, 'Округ': districts})

print(len(test_df))

test_df.to_csv("data_agro.csv", sep=',', index=False)
