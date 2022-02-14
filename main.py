
import urllib.request
from bs4 import BeautifulSoup

def crawl_a_page(url):
    #웹페이지의 소스를 가져온다.
    fp = urllib.request.urlopen(url)
    source = fp.read()
    fp.close()

    #소스에서 img_area 클래스 하위의 소스를 가져온다.
    soup = BeautifulSoup(source, 'html.parser')

    #이미지 경로를 받아온다.
    imgURL = soup.find_all("img")
    print(f'imgURL : {imgURL}')

    save_local = input('input local root folder : \n')
    print(f'save_local : {save_local}')
    for _idx, img in enumerate(imgURL):
        print(f'img : {img}')
        print(f'img.src : {img["src"]}')
        img_source_loc = img["src"]
        save_a_img(img_source_loc, save_local + '/' + str(_idx+1) + '.jpg')

def save_a_img(source_loc, file_name):
    urllib.request.urlretrieve(source_loc, file_name)

def action():
    tmpUrl = input('Please input the url you want to crawl : \n')
    crawl_a_page(tmpUrl)

if __name__ == '__main__':
    action()