# 觀看重點 #
## 查詢起始點 ##
1.  主要的觸發都寫在   if __name__ == '__main__': 這個名稱裡面
2.  然後在利用呼叫上面的function進行調用產出結果
3.  以ticketInfo這個function為例，我先去目標網站(ptt的日旅版)，我利用BeautifulSoup這個外界函數去抓他那一頁的網頁結果下來
4.  在利用soup.find_all這個功能把每個標題抓下來
5.  在利用foreach的功能一個一個把查到的結果與網址印出來
