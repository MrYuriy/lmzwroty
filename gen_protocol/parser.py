import requests
from bs4 import BeautifulSoup
import json


def get_name_sku_from_website_LM(sku):
    link = f"https://www.leroymerlin.pl/szukaj.html?q={sku}&sprawdz=true"
    name_of_product_and_sku =get_name_sku_of_product(link)
    return name_of_product_and_sku

def get_soup(url):
    r = requests.get(url )
    if r is None:
        return None
    else:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup


def get_name_sku_of_product(url):
    soup = get_soup(url)

    name_of_product = soup.findAll("script")
    result = {}
    for i in name_of_product:
        if "eanCode" in str(i):
            json_dikt = (json.loads(i.string))['props']['pageProps']["data"]["itemPage"]["content"][0]["listingProduct"]
            result["name_of_product"] = json_dikt["name"]
            result["sku"] = json_dikt["lmReference"]
    return result
    