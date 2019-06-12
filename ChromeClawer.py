from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

def catchWeb():
    GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = GOOGLE_CHROME_BIN
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

        # Webdriver 的執行檔也可以使用 PhantomJS
        # driver = webdriver.PhantomJS('phantomjs.exe')
        driver.maximize_window()
        driver.set_page_load_timeout(60)
        # driver.get(url)

        driver.get("https://zcaradmin.zerozero.com.tw/index")
        driver.find_element_by_name("userId").click()
        driver.find_element_by_name("userId").clear()
        driver.find_element_by_name("userId").send_keys("eric@df-recycle.com.tw")
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("yyy410591")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Welcome to ZEROZERO Administration'])[1]/following::button[1]").click()
        driver.find_element_by_link_text(u"管理員帳號管理").click()

        # 等待目標表格出現
        element = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, '00394@df-recycle.com.tw'))
        )
        # page_source 可以回傳目前瀏覽器所看到的網頁文件
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        td = soup.find(id='adminList_pager_right')
        count = td.find('div').string
        return count
    finally:
         print('end')
        #driver.quit()  # 關閉瀏覽器, 結束 webdriver process
