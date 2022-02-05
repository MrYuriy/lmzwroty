import re
from urllib import response
import requests
from bs4 import BeautifulSoup

def get_sku_from_website_LM(sku):
    
    link = f"https://www.leroymerlin.pl/szukaj.html?q={sku}&sprawdz=true"
    name_of_product =get_sku_name_of_product(link)
    
    return(name_of_product)

def get_soup(url):
    
    r = requests.get(url )
    
    if r == None:
        return None
    else:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup



def get_sku_name_of_product(url):
    soup = get_soup(url)

    name_of_product = soup.find('div', class_="product-description").find('div',class_="product-title" ).find('h1').string
    sku = int(soup.find('div', class_="product-description").find('div', class_="ref-number").find('span').string)
    resolt = {sku:name_of_product}
    #print("ok")
    #print(name_of_product)
    return(name_of_product)
get_sku_from_website_LM(83609035)