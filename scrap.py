import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import bs4
import time

base_url = "https://www.booking.com/searchresults.en-gb.html?ss=italy"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
chrome_opt = Options()
chrome_prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", chrome_prefs)
driver = webdriver.Chrome(options=chrome_opt)
driver.get(base_url)
time.sleep(5)

def get_base_page():
    page = driver.page_source
    flag_accepted = False
    urls = []
    while True:
        try:
            #process about Accept Button
            if "Accept" in page and flag_accepted is False:
                button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                button.click()
                flag_accepted = True

            #scroll down
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
            
            #get list about url of hotels
            soup = bs4.BeautifulSoup(page, "html.parser")
            url_els = soup.find_all("a", class_="a78ca197d0")

            url_len = len(url_els)
            print(url_len)
            if(url_len > 2000):
                return url_els
            
            #pagination process
            load_more_button = driver.find_element(By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.bf0537ecb5.f671049264.af7297d90d.c0e0affd09")
            load_more_button.click()
            time.sleep(2)

            page = driver.page_source
            
            # for i in url_els:
            #     temp = i["href"]
            #     urls.append(temp[:temp.find('label')-1])

        except NoSuchElementException:
            # No "Load More" button found, stop scrolling
            print("No more 'Load More' button found. Reached end of page.")
            break
        except ElementClickInterceptedException:
            # Handle case where something intercepts the click
            print("Click intercepted. Retrying after short delay.")
            time.sleep(5)
            continue
    
    return urls

def get_hotel_urls(page):
    soup = bs4.BeautifulSoup(page, "html.parser")
    url_els = soup.find_all("a", class_="a78ca197d0")
    urls = []
    for i in url_els:
        temp = i["href"]
        urls.append(temp[:temp.find('label')-1])
    return urls

def get_hotel_content(url):
    pass

if __name__ == "__main__":
    base_page = get_base_page()
    print(len(base_page))

  
    # rep = requests.get("https://www.booking.com/hotel/it/coccole-in-villa-b-amp-b-close-to-outlet.en-gb.html?aid=304142", headers=headers)
    # print(rep.text)