from bs4 import BeautifulSoup
from urllib import request
import requests
import random

def ticketInfo():
    inFo = ""
    resp = requests.get('https://www.ptt.cc/bbs/Japan_Travel/index.html')
    soup = BeautifulSoup(resp.text, 'html.parser')
    main_titles = soup.find_all('div', 'title')

    for title in main_titles:

        if "資訊" in title.text:
            inFo += title.text.strip() + "\n"
            inFo += "https://www.ptt.cc" + title.find("a")['href'] + "\n"

    return inFo

def imageInfo(url):
    print('IG url:' + url)
    imageUrl = ""
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    image = soup.find("meta", property="og:image")

    imageUrl = image["content"]
    print('image url:' + imageUrl)

    return imageUrl

def exchangeRate(country):
    rateString = ""
    resp = requests.get('http://www.findrate.tw/'+country+'/')
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    first_table = soup.find('table')
    index = 0
    main_tr = first_table.find_all('tr')
    for title in main_tr:
        index = index + 1
        if index == 2:
            temp = ""
            tdNum = 0
            main_td = title.find_all("td")
            for td in main_td:
                tdNum = tdNum + 1
                if tdNum != 4:
                    temp = temp + td.text + "|"

            temp = temp + "\n"
            rateString += temp

        if index == 3:
            temp = ""
            tdNum = 0
            main_td = title.find_all("td")
            for td in main_td:
                tdNum = tdNum + 1
                if tdNum != 4:
                    temp = temp + td.text + "|"

            temp = temp + "\n"
            rateString += temp

    rateString += "\n連結:http://www.findrate.tw/"+country+"/"
    return rateString

def fruitPrice(fruit):
    fruitString = ""
    resp = requests.get("https://www.twfood.cc/fruit/"+fruit+")")
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find_all('table', 'table-hover')
    main_tr = table[0].find_all('tr')

    index = 0
    temp = ""
    for tr in main_tr:
        if index%3 == 0:
            main_td = tr.find_all("th")
            if temp != "":
                temp +="\n"

            temp +=  main_td[0].text.strip()

        if index%3 == 1:
            main_str = tr.find_all("span")
            price = tr.find_all("th","vege_chart_th_unit")
            temp +="\n " + str(main_str[0].text).strip() +" "+ str(price[0].text).strip()

        if index%3 == 2:
            main_str = tr.find_all("span")
            price = tr.find_all("th","vege_chart_th_unit")
            temp +="\n " + str(main_str[0].text).strip() +" "+ str(price[0].text).strip()

        index = index + 1

    return temp



def getSebUrl(url):
    # 瀏覽器請求頭（大部分網站沒有這個請求頭可能會報錯）
    print(url)
    mheaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    req = request.Request(url,headers=mheaders) #新增headers避免伺服器拒絕非瀏覽器訪問
    page = request.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    body = soup.find(id="pins")
    link = body.find_all("li")
    next_link = []
    for li_element in link:
        # print(li_element.find('a').get('href'))
        next_link.append(li_element.find('a').get('href'))

    num = random.randint(1, len(next_link)-1)

    return next_link[num]  # python3 python2版本直接返回html

def getHtmlImgUrl(url):
    print(url)
    index = []
    mheaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    req = request.Request(url, headers=mheaders)  # 新增headers避免伺服器拒絕非瀏覽器訪問
    page = request.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    body = soup.find(class_="pagenavi")
    page = body.find_all("a")

    for page_element in page:
        # print(page_element.get('href').split('/'))
        element = page_element.get('href').split('/')
        if element[len(element)-1] != "":
            index.append(int(element[len(element)-1]))

    return url+"/"+str(random.randint(1, index[4]))

def getImage(url):
    print(url)
    mheaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    req = request.Request(url, headers=mheaders)  # 新增headers避免伺服器拒絕非瀏覽器訪問
    page = request.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    body = soup.find(class_='main-image')
    img = body.find('img').get('src')

    return  img

def getCk101Url(url):
    # 瀏覽器請求頭（大部分網站沒有這個請求頭可能會報錯）
    index = []
    mheaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    req = request.Request(url,headers=mheaders) #新增headers避免伺服器拒絕非瀏覽器訪問
    page = request.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    main = soup.find('div','bt-main-cont')
    search_li = main.find_all('li')
    for li in search_li:
        element = li.find('a').get('href')
        index.append(element)

    return index[random.randint(0, len(index)-1)]

def getCk101Photo(url):
    index = []
    mheaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    req = request.Request(url, headers=mheaders)  # 新增headers避免伺服器拒絕非瀏覽器訪問
    page = request.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    main_table = soup.find(id = 'lightboxwrap')
    img_all = main_table.find_all('img')

    for img in img_all:
        element = img.get('file')
        index.append(element)

    return index[random.randint(0, len(index)-1)]



# if __name__ == '__main__':
#     # Test Function
#     # IgUrl = "https://www.instagram.com/p/BymVt2NH5OE/?igshid=7jpeb1f596h6"
#     #IString = exchangeRate("JPY")
#     IArray = getCk101Photo(getCk101Url('https://ck101.com/beauty/'))
#     # IArray = getImage('https://www.mzitu.com/187752/16')
#
#     print(IArray)
