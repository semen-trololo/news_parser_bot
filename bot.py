# pip install requests
# pip install beautifulsoup4
# pip install pytelegrambotapi

import telebot
import requests
from bs4 import BeautifulSoup
import time
import difflib

headers_3dnews = []
headers_4pda = []
headers_xaker = []
bot = telebot.TeleBot('')


def send_teleg_bot(message):
    bot.send_message(chat_id='@', text=message)


def similarity(s1, s2):
  normalized1 = s1.lower()
  normalized2 = s2.lower()
  matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
  return matcher.ratio()


def search_duplicates(text_news):
    for tmp in headers_3dnews:
        value = similarity(text_news, tmp)
        if value > 0.55:
            send_teleg_bot('[DEBUG]Возможно вы это уже видели :) \n[DEBUG]' + str(value) + '\n [DEBUG]' + str(tmp) + '\n' + '[DEBUG]' + str(text_news) + '\n')
            return True
    for tmp in headers_4pda:
        value = similarity(text_news, tmp)
        if value > 0.55:
            send_teleg_bot('[DEBUG]Возможно вы это уже видели :) \n[DEBUG]' + str(value) + '\n [DEBUG]' + str(tmp) + '\n' + '[DEBUG]' + str(text_news) + '\n')
            return True
    for tmp in headers_xaker:
        value = similarity(text_news, tmp)
        if value > 0.55:
            send_teleg_bot('[DEBUG]Возможно вы это уже видели :) \n[DEBUG]' + str(value) + '\n [DEBUG]' + str(tmp) + '\n' + '[DEBUG]' + str(text_news) + '\n')
            return True
    return False


def parse_3dnews(ferst_start):
    try:
        r = requests.get('https://3dnews.ru/news')
    except:
        print('[DEBUG] Error get URL')
        send_teleg_bot('[DEBUG] Error get URL 3dnew')
        return False
    #r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, "html.parser")
    soup_blok = soup.find_all('div', {'class': "cntPrevWrapper"})
    tmp_time = time.time()
    for tmp in soup_blok:
        try:
            data_news = tmp.find('span').string
            link = tmp.find('a', {'class': "entry-header"})
            link_news = link.get('href')
            if 'http' in link_news:
                pass
            else:
                link_news = 'https://3dnews.ru' + link_news
            text_news = tmp.find('h1').string
            text_news = text_news.replace('\xa0', ' ')
            text_news = text_news.strip()
            data_news = time.strptime(data_news, '%d.%m.%Y %H:%M ')
        except:
            continue
        if ferst_start:
            if link_news not in headers_3dnews:
                headers_3dnews.append(text_news)
        else:
            if text_news not in headers_3dnews:
                if data_news.tm_mday == time.gmtime(tmp_time).tm_mday:
                    try:
                        search_duplicates(text_news)
                    except:
                        send_teleg_bot('[DEBUG] Error duplicates')
                    try:
                        send_teleg_bot(link_news)
                        headers_3dnews.append(text_news)
                    except:
                        print('[DEBUG] Error send in telegram')
    #print(headers_3dnews)
    return True


def parse_4pda(ferst_start):
    tmp_time = time.time()
    try:
        r = requests.get('https://4pda.to')
    except:
        print('[DEBUG] Error get URL 4pda')
        send_teleg_bot('[DEBUG] Error get URL 4pda')
        return False
    # r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, "html.parser")
    soup_blok = soup.find_all('article')
    for tmp in soup_blok:
        try:
            link = tmp.find('a')
            link_news = link.get('href')
            text_news = link.get('title')
            text_news = text_news.strip()
            data_tmp = tmp.find('em', {'class': "date"}).string
            data_tmp = data_tmp.split('.')
            data_tmp[2] = '20' + data_tmp[2]
            data_tmp = data_tmp[0] + '.' + data_tmp[1] + '.' + data_tmp[2]
            data_news = time.strptime(data_tmp, '%d.%m.%Y')
        except:
            continue
        if ferst_start:
            if data_news.tm_mday == time.gmtime(tmp_time).tm_mday:
                headers_4pda.append(text_news)
        else:
            if text_news not in headers_4pda:
                if data_news.tm_mday == time.gmtime(tmp_time).tm_mday:
                    try:
                        search_duplicates(text_news)
                    except:
                        send_teleg_bot('[DEBUG] Error duplicates')
                    try:
                        send_teleg_bot(link_news)
                        headers_4pda.append(text_news)
                    except:
                        print('[DEBUG] Error send in telegram')
    #print(headers_4pda)
    return True


def parse_xaker(ferst_start):
    tmp_time = time.time()
    try:
        r = requests.get('https://xakep.ru/')
    except:
        print('[DEBUG] Error get URL')
        send_teleg_bot('[DEBUG] Error get URL xakep')
        return True
    # r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, "html.parser")
    soup_blok = soup.find_all('div', {'class': "block-article-content-wrapper"})
    for tmp in soup_blok:
        try:
            link = tmp.find('h3', {'class': "entry-title"})
            link_a = link.find('a')
            link_news = link_a.get('href')
            text_news = link.find('span').string
            text_news = text_news.strip()
            data_tmp = link_news.split('/')
            data_tmp = data_tmp[5] + '.' + data_tmp[4] + '.' + data_tmp[3]
            data_news = time.strptime(data_tmp, '%d.%m.%Y')
        except:
            continue
        if ferst_start:
            if text_news not in headers_xaker:
                headers_xaker.append(text_news)
        else:
            if text_news not in headers_xaker:
                if data_news.tm_mday == time.gmtime(tmp_time).tm_mday:
                    try:
                        search_duplicates(text_news)
                    except:
                        send_teleg_bot('[DEBUG] Error duplicates')
                    try:
                        send_teleg_bot(link_news)
                        headers_xaker.append(text_news)
                    except:
                        print('[DEBUG] Error send in telegram')

    return True


def start(flag, ferst_star):
    while True:
        if parse_3dnews(ferst_star):
            if parse_4pda(ferst_star):
                if parse_xaker(ferst_star):
                    ferst_star = False
                    if flag:
                        send_teleg_bot('Start parser bot.')
#                       print('Start')
                    break
        headers_3dnews = []
        headers_4pda = []
        headers_xaker = []
        time.sleep(10)
    return ferst_star


ferst_star = start(True, True)
while True:
#    print('++++')
    if len(headers_3dnews) >= 300:
        print('[DEBUG] Len headers > 300, clear')
        send_teleg_bot('[DEBUG] Len headers > 300, clear')
        headers_3dnews = []
        headers_4pda = []
        headers_xaker = []
        tmp = str(len(headers_3dnews))
        send_teleg_bot(f'[DEBUG] Len->{tmp}')
        ferst_star = start(False, ferst_star)
    parse_3dnews(ferst_star)
    parse_4pda(ferst_star)
    parse_xaker(ferst_star)
    time.sleep(600)
