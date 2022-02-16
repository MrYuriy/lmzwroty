import re
from urllib import response
import requests
from bs4 import BeautifulSoup

def get_name_sku_from_website_LM(sku):
    
    link = f"https://www.leroymerlin.pl/szukaj.html?q={sku}&sprawdz=true"
    name_of_product_and_sku =get_name_sku_of_product(link)
    
    return(name_of_product_and_sku)

def get_soup(url):
    
    r = requests.get(url )
    
    if r == None:
        return None
    else:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup



def get_name_sku_of_product(url):
    soup = get_soup(url)

    name_of_product = soup.find('div', class_="product-description").find('div',class_="product-title" ).find('h1').string
    sku = int(soup.find('div', class_="product-description").find('div', class_="ref-number").find('span').string)
    resolt = {"name_of_product":name_of_product, "sku":sku}
    #print("ok")
    print(sku)
    #print(name_of_product)
    return(resolt)
#def get_sku_ean(url):
    