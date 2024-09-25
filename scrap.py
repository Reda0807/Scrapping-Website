import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
import time

base_url = "https://www.booking.com/searchresults.en-gb.html?ss=italy"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
driver = webdriver.Chrome()
driver.get(base_url)
page = driver.page_source

def get_base_page():
    scroll_to_bottom()
    
    return page

def get_hotel_urls(page):
    soup = bs4.BeautifulSoup(page, "html.parser")
    url_els = soup.find_all("a", class_="a78ca197d0")
    urls = []
    for i in url_els:
        temp = i["href"]
        urls.append(temp[:temp.find('label')-1])
    return urls

def scroll_to_bottom():
    while True:
        if "Accept" in page:
            button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            button.click()

        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(5)

        print("Load more results" in page)
        if "Load more results" in page:
            break

def get_hotel_content(url):
    pass

if __name__ == "__main__":
    base_page = get_base_page()
    print(len(get_hotel_urls(base_page)))

  
    # rep = requests.get("https://www.booking.com/hotel/it/coccole-in-villa-b-amp-b-close-to-outlet.en-gb.html?aid=304142", headers=headers)
    # print(rep.text)