
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import time
import re
import seaborn
from lxml import html
import matplotlib


from pylab import rcParams
rcParams['figure.figsize'] = 8, 5

s = requests.Session()
s.headers.update({
    'Referer': 'http://www.calend.ru',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 YaBrowser/18.10.2.163 Yowser/2.5 Safari/537.36'
})

def load_user_data(session):
    url = 'http://www.calend.ru'
    request = session.get(url)
    return request.text

def contain_movies_data(text):
    soup = BeautifulSoup(text,"html.parser")
    holidays_list = soup.find('div',{'class':'w01'})
    return holidays_list is not None

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def parse_user_datefile_bs(filename):
    results=[]
    text = read_file(filename)

    soup = BeautifulSoup(text,"html.parser")
    holidays_list = soup.find('div',{'class':'famous-date plusyear2 leftim'})
    holidays_list = holidays_list.find('div',{'class':'w01'}).find_all('a')
    #results.append(holiday_names.text)
    for item in holidays_list:
         results.append(item.text)
    return results

data = load_user_data(s)
if(contain_movies_data(data)):
    with open('./holidays_data/birthlist.html', 'wb') as output_file:
        output_file.write(data.encode('cp1251'))

results = []
#for filename in os.listdir('./holidays_data/'):
#    results.extend(parse_user_datefile_bs('./holidays_data/'+filename))

results.extend(parse_user_datefile_bs('./holidays_data/birthlist.html'))

results = list(filter(None, results))

holidays_data_df = pd.DataFrame(results)

print(results)


