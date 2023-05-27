import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_name(soup):
    try:
        name = soup.find("span",attrs={'class':'a-size-large product-title-word-break'})
        name_value = name.text.strip()
    except AttributeError:
        name_value = None
    return name_value
def get_price(soup):
    try:
        price = soup.find("span",attrs={'class':'a-price-whole'})
        price_value = price.text.strip()
    except AttributeError:
        price_value = None
    return price_value
def get_rating(soup):
    try:
        rateing = soup.find("span",attrs={'class':'a-size-medium a-color-base'})
        rating_value = rateing.text
    except AttributeError:
        rating_value = None
    return rating_value
def get_review(soup):
    try:
        num_of_rev = soup.find("span",attrs={'id':'acrCustomerReviewText','class':"a-size-base"})
        num_of_rev_fetch = num_of_rev.text.strip()
        num_of_rev_value = num_of_rev_fetch.replace("ratings","reviews")
    except AttributeError:
        num_of_rev_value = None
    return num_of_rev_value


def get_Description(soup):
    try:
        description = soup.find("span",attrs={'class':"a-size-large product-title-word-break"})
        description_value = description.text.strip()
    except AttributeError:
        description_value = None
    return description_value
def get_ASIN(soup):
    try:
        asin = soup.find("ul",attrs={'class':'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'})
        table = asin.find_all("li")
        asin_value = ''
        for li in table:
            s = li.find("span",attrs={'class':'a-text-bold'})
            string = "ASIN"
            if string in s.text:
                asin_value = li.text.strip()
    except AttributeError:
        asin_value = None
    return asin_value
def get_Product_Description(soup):
    try:
        product_desc = soup.find("ul",attrs={'class':'a-unordered-list a-vertical a-spacing-mini'})
        product_desc_value = product_desc.text.strip()
    except AttributeError:
        product_desc_value = None
    return product_desc_value
def get_Manufacturer(soup):
    try:
        manufacturer = soup.find("ul",attrs={'class':'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'})
        table = manufacturer.find_all("li")
        manufacturer_value = ''
        for li in table:
            s = li.find("span",attrs={'class':'a-text-bold'})
            string = "Manufacturer"
            if string in s.text:
                manufacturer_value = li.text.strip()
    except AttributeError:
        manufacturer_value = None 
    return manufacturer_value


Product_URL=[]
Product_Name=[]
Product_Price=[]
Rating=[]
Number_of_reviews=[]

Description=[]
ASIN=[]
Product_Description=[]
Manufacturer=[]
header = ({'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",'Accept-Language': 'en-US, en;q=0.5'})
for page in range(1,25):
    req = requests.get("https://www.amazon.in/s?k=bags&page="+str(page)+"&crid=2M096C61O4MLT&qid=1685113589&sprefix=ba%2Caps%2C283&ref=sr_pg_"+str(page),headers=header)
    soup = bs(req.content , 'html.parser')
    urls = soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
    for link in urls:
        url = link.get("href")
        product_url = "https://www.amazon.in/"+url
        Product_URL.append(product_url)
        new_req = requests.get(product_url,headers=header)
        new_soup = bs(new_req.content , "html.parser")
        
        Product_Name.append(get_name(new_soup))
        Product_Price.append(get_price(new_soup))
        Rating.append(get_rating(new_soup))
        Number_of_reviews.append(get_review(new_soup))
        
        Description.append(get_Description(new_soup))
        ASIN.append(get_ASIN(new_soup))
        Product_Description.append(get_Product_Description(new_soup))
        Manufacturer.append(get_Manufacturer(new_soup))
        
df = pd.DataFrame({'URL':Product_URL,'Name':Product_Name,'Price':Product_Price,'Rating':Rating,'Review':Number_of_reviews}) 
df.to_csv('Product_List.csv', index=False, header=True)
df = pd.DataFrame({'Description':Description,'ASIN':ASIN,'Product_Description':Product_Description,'Manufacturer':Manufacturer}) 
df.to_csv('Product_Description_List.csv', index=False, header=True)