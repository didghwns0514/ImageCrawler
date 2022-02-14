# from bs4 import BeautifulSoup
# import requests
# from selenium import webdriver
#
# URL = 'https://www.29cm.co.kr/product/1230341'
# driver = webdriver.Chrome(executable_path='./chromedriver-intel')
# driver.get(url=URL);

from selenium import webdriver
import urllib.request
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import concurrent.futures
import requests
from PIL import Image, ImageFile
import lxml
from pathlib import Path
import os
from datetime import datetime, timedelta


class Selenium:
    # @ setup args
    # location = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "static", "chromedriver")
    LOCATION = './chromedriver-intel'
    OPTIONS = webdriver.ChromeOptions()
    ARGS = ['headless', 'window-size=1920x1080', 'disable-gpu',
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"]
    for arg in ARGS:
        OPTIONS.add_argument(arg)

    def __init__(self):
        # @ driver
        print(f'selenum driver location : {Selenium.LOCATION}')

        # initialize chrome driver
        self.driver = webdriver.Chrome(Selenium.LOCATION, chrome_options=Selenium.OPTIONS)
        self.driver.implicitly_wait(3)

    def action(self):
        tmpInput = input('input the url you want to crawl : \n')

        self.setDriver(tmpInput)
        self.runCrawler(tmpInput)

    def setDriver(self, url: str):
        """load driver a url"""
        try:
            # print(f'SeleniumUpdater.driver : {SeleniumUpdater.driver}')
            # print(f'type(SeleniumUpdater.driver) : {type(SeleniumUpdater.driver)}')
            if self.driver.current_url != url:
                self.driver.get(url)
        except:
            pass

    def runCrawler(self, targUrl: str = None):
        """"""

        self.setDriver(targUrl)
        self.runBS4(self.driver.page_source)
        self.driver.close()

    def runBS4(self, htmlSource):

        image_counter = 0
        soup = BeautifulSoup(htmlSource, 'lxml')
        imgURL = soup.find_all("img")

        save_local = input('input local root folder : \n')
        print(f'save_local : {save_local}')

        for _idx, img in enumerate(imgURL):
            print(f'img : {img}')
            print(f'img.src : {img["src"]}')
            img_source_loc = img["src"]

            try:
                sourceValidation = isURLValid(img_source_loc)
                print(f'sourceValidation 1 : {sourceValidation}')
            except Exception as e1:
                print(f'error - 1 : {e1}')
                try:
                    img_source_loc = 'https:' + img_source_loc
                    sourceValidation = isURLValid(img_source_loc)
                    print(f'sourceValidation 2 : {sourceValidation}')
                except Exception as e2:
                    print(f'error - 2 : {e2}')
                    continue

            if sourceValidation:
                image_counter += 1
                if image_counter > 20 :
                    break
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    try:
                        executor.submit(save_a_img,
                                        img_source_loc, save_local + '/' + str(image_counter) + '.jpg'
                                        )
                    except Exception as e1:
                        print(f'error - 1 : {e1}')


def isURLValid(url:str):
    res = requests.get(url, stream=True)
    isValid, imgSize = check_img_size(url)
    if isValid:
        print(f'imgSize : {imgSize}')
        if imgSize[0] >= 400 and imgSize[1] >= 400:
            count = 1
            while True:
                if res.status_code != 200 : # Not valid
                    if count <= 5:
                        res = requests.get(url, stream=True)
                        print(f'Retry: {count} {url}')
                        count += 1
                    else:
                        return False
                else:
                    return True
        else:
           return False
    return False

def check_img_size(url:str):
    resume_header = {'Range': 'bytes=0-2000000'}  ## the amount of bytes you will download
    data = requests.get(url, stream=True, headers=resume_header).content

    p = ImageFile.Parser()
    p.feed(data)  ## feed the data to image parser to get photo info from data headers
    if p.image:
        return True, p.image.size  ## get the image size (Width, Height)
    return False, None

def save_a_img(source_loc, file_name):
    # img = Image.open(source_loc)
    # print(f'img : {img.size[0]}  / {img.size[1]}')

    urllib.request.urlretrieve(source_loc, file_name)

if __name__ == '__main__':
    tmpSelenium = Selenium()
    tmpSelenium.action()