import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
import time

#Configure the WebDriver
def setup_driver():
    chrome_opt = Options()
    chrome_prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_opt.add_experimental_option("prefs", chrome_prefs)
    driver = webdriver.Chrome(options=chrome_opt)
    return driver

def get_base_page(driver, base_url):
    driver.get(base_url)
    time.sleep(5)
    page = driver.page_source
    flag_accepted = False
    
    while True:
        try:
            #process about Accept Button
            if "Accept" in page and flag_accepted is False:
                button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                button.click()
                flag_accepted = True

            #scroll down
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(5)
            
            #get list about url of hotels
            soup = bs4.BeautifulSoup(page, "html.parser")
            url_els = soup.find_all("a", class_="a78ca197d0")

            url_len = len(url_els)
            if(url_len > 100):
                return url_els
            
            #pagination process
            load_more_button = driver.find_element(By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.bf0537ecb5.f671049264.af7297d90d.c0e0affd09")
            load_more_button.click()
            time.sleep(5)

            page = driver.page_source

        except NoSuchElementException:
            # No "Load More" button found, stop scrolling
            print("No more 'Load More' button found. Reached end of page.")
            break
        except ElementClickInterceptedException:
            # Handle case where something intercepts the click
            print("Click intercepted. Retrying after short delay.")
            time.sleep(5)
            continue
    
    return url_els

def get_hotel_data(driver, hotel_list):
    hotel_data = {}
    hotels = []
    for i in hotel_list:
        temp = i["href"]
        url = temp[:temp.find('label')-1]

        driver.get(url)
        try:
            wait = WebDriverWait(driver, 30)

            #get Hotel Category
            category_temp = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.bui_breadcrumb__link_masked'))).text
            hotel_category = re.search(r"\(([^)]+)\)", category_temp).group(1)

            #get Hotel Name
            hotel_name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.d2fee87262.pp-header__title'))).text
            
            #get Hotel Address
            hotel_address = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip'))).text.replace('\n','').strip()
            
            #get Hotel Coordenadas Maps
            hotel_map_style = re.search(r'url\((.*?)\)', wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.eec927a9a4'))).get_attribute('style')).group(1).strip("'\"")

            #get Hotel Public Website
            hotel_url = url

            #get Hotel Fotos
            hotel_photos = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.clearfix.bh-photo-grid.fix-score-hover-opacity')))
            photo_lists = hotel_photos.find_elements(By.TAG_NAME, 'a')
            photo_len = len(photo_lists)
            
            if photo_len > 5:
                photo_lists = photo_lists[:5]
            photo_urls = []

            for photo in photo_lists:
                photo_temp = re.search(r'url\((.*?)\)', photo.get_attribute('style')).group(1).strip("'\"")
                
                if photo_temp:
                    photo_urls.append(photo_temp)
                else:
                    photo_urls.append("None")
            hotel_photo_urls = "\n".join(photo_urls)

            
            print(f"Categoria: {hotel_category}")
            print(f"hotel_name: {hotel_name}")
            print(f"hotel_address: {hotel_address}")
            print(f"hotel_map: {hotel_map_style}")
            print(f"hotel_url: {hotel_url}")
            print(f"hotel_photo_urls: {hotel_photo_urls}")
                      
        except Exception as e:
            print(f"An error occurred fetching the hotel name: {e}")

        # response = requests.get(url)
        # html_content = response.content
        # soup = bs4.BeautifulSoup(html_content, 'html.parser')

        # #get hotel_name
        # category_temp = soup.select_one('a.bui_breadcrumb__link_masked').text
        # hotel_category = re.search(r"\(([^)]+)\)", category_temp).group(1)
        # hotel_name = soup.select_one('h2.d2fee87262.pp-header__title').text
        # hotel_address = soup.select_one('span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip').text.replace('\n','').strip()
        # hotel_map = soup.find('div', class_='eec927a9a4').get('style')
        
        # hotel_map_url = re.search(r'url\((.*?)\)', hotel_map).group(1).strip("'\"")
        


        time.sleep(5)
        break

if __name__ == "__main__":
    base_url = "https://www.booking.com/searchresults.en-gb.html?ss=italy"
    driver = setup_driver()
    hotel_list = get_base_page(driver,base_url)
    get_hotel_data(driver,hotel_list)
  
    # rep = requests.get("https://www.booking.com/hotel/it/coccole-in-villa-b-amp-b-close-to-outlet.en-gb.html?aid=304142", headers=headers)
    # print(rep.text)