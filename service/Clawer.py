from bs4 import BeautifulSoup
import requests

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
# if __name__ == '__main__':
#     # Test Function
#     # IgUrl = "https://www.instagram.com/p/BymVt2NH5OE/?igshid=7jpeb1f596h6"
#     #IString = exchangeRate("JPY")
#     IString = fruitPrice()
#     print(IString)
